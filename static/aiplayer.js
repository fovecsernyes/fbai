/// @file aiplayer.js
//  @author Mark Vecsernyes
//
//  @brief This file contains the "AIPLAYER MODE"
//  @{

/// Post request to /ai/startgen after every generation
//  calls rungame() method
var start_gen = function(){
        $.ajax({
            type: "POST",
            url: "/ai/startgen",
            contentType: "application/json",
            data: JSON.stringify( {"request" : "startgen"} ),
            dataType: "json",
            async: false,
            success: function(response) {
                //console.log(response);
                rungame(response);
            },
            error: function(err) {
                alert("Server side error");
            },
            timeout: 5000 //timeout for 5 sec
        });
}


/// Loading pictures
var LoadImages = function () {
    bg = new Image();
    fg = new Image();
    welcome = new Image();

    bg.src = "/static/images/bg.png";
    welcome.src="/static/images/welcome.png"

    bird = new Image();
    pipeNorth = new Image();
    pipeSouth = new Image();
    bird.src = "/static/images/bird.png";
    pipeNorth.src = "/static/images/pipeNorth.png";
    pipeSouth.src = "/static/images/pipeSouth.png";

    return self;
}


/// Birds class
//  @param db_id string the id of the birds
var Bird = function (db_id) {
    var self = {
        bX: 10,
        bY: 150,
        id: db_id,
        fitness: 0,
        alive: true
    }
    /// Updating birds
    //  @param gravity integer
    //  @param command list [0, 1, .. 1, 0]
    //  @param jump integer jumping height
    self.update = function (gravity, command, jump) {
        self.fitness++;
        self.bY += gravity;
        if(command){
            self.moveUp(jump);
        }
    }
    /// Moving up
    //  @param jump integer
    self.moveUp = function (jump) {
        self.bY -= jump;
    }

    return self;
}


/// Pipe class
//  @param y integer the center of the pipe
var Pipe = function (y) {
    var self =
    {
        pX: cvs.width/2,
        pY: y
    }
    //update the pipes 
    self.update = function () {
        self.pX--;
    }
    return self;
}


var best_fitness = 0;
var best_gen = 0;


/// Game class
//  @param response running_params 
var Game = function (response) {
    //variables mainly from backend response
    var fitness_scores = [];
    var gravity = response["gravity"]/5;
    var population = response["population"];
    var gap = response["gap"];
    var jump = response["jump"];
    var distance = 288 - response["distance"];
    var birds_ids = JSON.parse(response["bird_ids"]);
    var generation = parseInt(response["generation"]);
    var bird_begin = parseInt(birds_ids[0]);
    var bird_end = parseInt(birds_ids[population-1]);
    var command = new Array(population).join(0).split('');
    var threshold = parseInt(response["threshold"]);
    var threshold_met = false;

    var img = LoadImages();

    var bird = [];
    for (var i = bird_begin; i <= bird_end; i++) {
        bird[i] = Bird(i);
    }

    var pipe = [];
    var min = -256 + 150;
    var max = 0;
    pipe[0] = Pipe( Math.random() * (max - min) + min);
    var alive = population;


    /// Updating game
    //  sends a post request to /ai/jumbird in every moment to get the commands
    //  when all birds die it sends post reques with the fitness values to /ai/finishgen
    self.update = function () {
        if (alive > 0) {
            alive = 0;
            ctx.drawImage(img.bg, 0, 0);

            for (var i = 0; i < pipe.length; i++) {
                if (pipe[i].pX < 0 - img.pipeNorth.width) {
                    pipe.shift();
                }
                
                constant = img.pipeNorth.height + gap;
                ctx.drawImage(img.pipeNorth, pipe[i].pX, pipe[i].pY);
                ctx.drawImage(img.pipeSouth, pipe[i].pX, pipe[i].pY + constant);
                
                ctx.drawImage(img.welcome, canvas.width/2, 0);
                
                pipe[i].update();

                if (pipe[i].pX == distance) { 
                    pipe.push(Pipe( Math.random() * (max - min) + min ));
                }

            }

            ctx.fillStyle="black";
            ctx.font="14px Monospace";
            ctx.textAlign = "left";
            ctx.fillText("Best: " + best_fitness + ' at ' + best_gen + '. gen', 0, cvs.height - 10);

            ctx.fillStyle="blue";
            ctx.font="12px Monospace";
            ctx.textAlign = "center";
            ctx.fillText(generation + " .  G E N E R A T I O N", cvs.width/4 * 3, 10);

            request = [];
            for (var i = bird_begin; i <= bird_end; i++) {
                if (bird[i].alive) {
                    request.push(i + '#' + parseInt(bird[i].bY) + ',' + pipe[0].pX + ',' + (pipe[0].pY + constant));
                }else{
                    request.push(i + '#' + 'dead');
                }

                if (bird[i].alive) {
                    bird[i].update(gravity, command[i-bird_begin], jump);

                    ctx.drawImage(img.bird, bird[i].bX, bird[i].bY);
                    for (var j = 0; j < pipe.length; j++) {
                        if (bird[i].bX + img.bird.width >= pipe[j].pX && bird[i].bX <= pipe[j].pX + img.pipeNorth.width && (bird[i].bY <= pipe[j].pY + img.pipeNorth.height || bird[i].bY + img.bird.height >= pipe[j].pY + constant) || bird[i].bY + img.bird.height >= cvs.height - fg.height) {
                            bird[i].alive = false;
                            if (fitness_scores[i] == null){
                                fitness_scores[i] = bird[i].fitness;
                            }else{
                                fitness_scores[i] += bird[i].fitness;
                            }
                        }
                    }
                }

                if(bird[i].alive){
                    alive++;
                }

                var c = i - bird_begin;

                if (c < 10 ){
                    c = "0" + c;
                }

                ctx.font="12px Monospace";
                ctx.textAlign = "left";

                if(bird[i].alive){
                    ctx.fillStyle="black";
                }else{
                    ctx.fillStyle= "red";
                }
                if( (i - bird_begin + 1) <= 50 ){
                    ctx.fillText(c + ". score: " + bird[i].fitness, cvs.width/2 + 2, 20 + c*10);
                }else{
                    ctx.fillText(c + ". score: " + bird[i].fitness, cvs.width/2 + 150, 20 + (c-50)*10);
                }

                ctx.beginPath();
                ctx.moveTo(cvs.width/2,0);
                ctx.lineTo(cvs.width/2,cvs.height);
                ctx.stroke();

                if(bird[i].fitness > best_fitness){
                    best_fitness = bird[i].fitness;
                    best_gen = generation;
                }

                if(bird[i].fitness >= threshold){
                    threshold_met = true;
                }
            }

            if(threshold_met){
                ctx.fillStyle="red";
                ctx.font="20px Monospace";
                ctx.textAlign = "center";
                ctx.fillText("Threshold met", cvs.width/4, cvs.height/2);
                return;
            }

            $.ajax({
                    type: "POST",
                    url: "/ai/jumpbird",
                    contentType: "application/json",
                    data: JSON.stringify( request ),
                    dataType: "json",
                    async: false,
                    success: function(response) {
                        for(var i = 0; i < response.length; i++){
                            command[i] = parseInt( response[i] );
                        }
                        requestAnimationFrame(update);
                    },
                    error: function(err) {
                        alert("Server side error");
                    },
                    timeout: 5000 //timeout for 5 sec
                });

        }else{
            request = [];
            for (var i = bird_begin; i <= bird_end; i++){

                request.push(i + "#" + bird[i].fitness);
            }
            $.ajax({
                    type: "POST",
                    url: "/ai/finishgen",
                    contentType: "application/json",
                    data: JSON.stringify( request ),
                    dataType: "json",
                    async: false,
                    success: function(response) {
                        //console.log(response);
                        start_gen();
                    },
                    error: function(err) {
                        alert("Server side error");
                    },
                    timeout: 5000 //timeout for 5 sec
                });
            
        }
    }
    return self;
}


/// Run the game
var rungame =function(response){
    var game = Game(response);
    game.update();
}

/// @}