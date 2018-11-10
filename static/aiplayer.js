/// @file aiplayer.js
//  @author Mark Vecsernyes
//
//  @brief This file contains the "AIPLAYER MODE"
//  @{

/// dropdown list
var show_label = function(){
    label[0] =  $('#gra_dd').val();
    label[1] = $('#jum_dd').val();
    label[2] = $('#pop_dd').val();
    label[3] = $('#gap_dd').val();
    label[4] = $('#dis_dd').val();
        
    label[5] = $('#hid_dd').val();
    label[6] = $('#sel_dd').val();
    label[7] = $('#del_dd').val();
    label[8] = $('#cro_dd').val();
    label[9] = $('#mu1_dd').val();
    label[10] = $('#mu2_dd').val();

    $('#gra_dd').val("Gravity");
    $('#jum_dd').val("Jump");
    $('#pop_dd').val("Population");
    $('#gap_dd').val("Gap");
    $('#dis_dd').val("Distance");

    $('#hid_dd').val("Hidden neurons");
    $('#sel_dd').val("Selection rates");
    $('#del_dd').val("Deletion rate");
    $('#cro_dd').val("Crossover rate");
    $('#mu1_dd').val("Mutation rate on population");
    $('#mu2_dd').val("Mutation rate on entity");

}

var hide_label = function(){
    $('#gra_dd').val(label[0]);
    $('#jum_dd').val(label[1]);
    $('#pop_dd').val(label[2]);
    $('#gap_dd').val(label[3]);
    $('#dis_dd').val(label[4]);

    $('#hid_dd').val(label[5]);
    $('#sel_dd').val(label[6]);
    $('#del_dd').val(label[7]);
    $('#cro_dd').val(label[8]);
    $('#mu1_dd').val(label[9]);
    $('#mu2_dd').val(label[10]);
}

/// Initializing dropdown list
//  @param begin integer
//  @param end integer
//  @param add integer 
//  @param label string
//  @return options string
var dropdown = function(begin, end, add, label){
    options = "<option disabled>" + label + "</option>";
    for(var i=begin; i<=end; i=i+add){
        options += "<option>"+ i +"</option>";
    }
    return options;
}

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
                console.log(response);
                rungame(response);
            },
            error: function(err) {
                console.log(err || 'Error!');
            }
        });
}

var best_fitness = 0;

/// Loading pictures
var LoadImages = function () {
    bg = new Image();
    fg = new Image();
    welcome = new Image();

    bg.src = "/static/images/bg.png";
    fg.src = "/static/images/fg.png";
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

/// Gae class
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

    var img = LoadImages();


    var bird = [];
    for (var i = bird_begin; i <= bird_end; i++) {
        bird[i] = Bird(i);
    }

    var pipe = [];
    max = -50;
    min = -256 + 100
    pipe[0] = Pipe( Math.random() * (max - min) + min);
    console.log( img.pipeNorth.height )
    alive = population;
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
            ctx.drawImage(img.fg, 0, cvs.height - img.fg.height);

            ctx.fillStyle="black";
            ctx.font="14px Monospace";
            ctx.textAlign = "left";
            ctx.fillText("Best: " + best_fitness, 0, cvs.height - 10);

            ctx.fillStyle="blue";
            ctx.font="12px Monospace";
            ctx.textAlign = "left";
            ctx.fillText(generation + ". GENERATION", cvs.width/2 + 20, 10);

            request = [];
            for (var i = bird_begin; i <= bird_end; i++) {
                if (bird[i].alive) {
                    request.push(i + '#' + parseInt(bird[i].bY) + ',' + pipe[0].pX + ',' + (pipe[0].pY + constant));
                }else{
                    request.push(i + '#' + 'dead');
                }
            }
            for (var i = bird_begin; i <= bird_end; i++) {
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
                    ctx.fillText(c + ". fitness: " + bird[i].fitness, cvs.width/2 + 20, 20 + c*10);
                }else{
                    ctx.fillText(c + ". fitness: " + bird[i].fitness, cvs.width/2 + 170, 20 + (c-50)*10);
                }

                ctx.beginPath();
                ctx.moveTo(cvs.width/2,0);
                ctx.lineTo(cvs.width/2,cvs.height);
                ctx.stroke();
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
                        console.log(err || 'Error!');
                    }
                });

        }else{
            request = [];
            for (var i = bird_begin; i <= bird_end; i++){

                if(bird[i].fitness > best_fitness){
                    best_fitness = bird[i].fitness;
                }

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
                        console.log(response);
                        start_gen();
                    },
                    error: function(err) {
                        console.log(err || 'Error!');
                    }
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