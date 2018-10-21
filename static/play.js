//this is the frontend script file

//dropdown menu
var dropdown = function(begin, end, add){
    var options = "";
    for(var i=begin; i<=end; i=i+add){
        options += "<option>"+ i +"</option>";
    }
    return options;
}

//function for /startgen post request, this starts the a new generation
var start_gen = function(){
        $.ajax({
            type: "POST",
            url: "/startgen",
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

//function for loading images
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

//class for Birds
var Bird = function (db_id) {
    var self = {
        bX: 10,
        bY: 150,
        id: db_id,
        fitness: 0,
        alive: true
    }
    //update function, the command can be 0 or 1, depends on the neural network
    self.update = function (gravity, command) {
        self.fitness++;
        self.bY += gravity;
        if(command){
            self.moveUp();
        }
    }
    //funtion for moving up
    self.moveUp = function () {
        self.bY -= 25;
    }
    //function for killing a bird
    self.kill = function () {
        self.alive = false;
    }

    return self;
}

//class for Pipes
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
//Game class which handles almost everything
var Game = function (response) {
    //variables mainly from backend response
    var fitness_scores = [];
    var gravity = response["gravity"]/5;
    var population = response["population"];
    var gap = response["gap"];
    var distance = 288 - response["distance"];
    var birds_ids = JSON.parse(response["bird_ids"]);

    console.log(birds_ids);

    var bird_begin = parseInt(birds_ids[0]);
    var bird_end = parseInt(birds_ids[population-1]);
    var command = new Array(population).join(0).split('');
    //loading the images
    var img = LoadImages();
    //creating the first pipe
    var pipe = [];
    pipe[0] = Pipe(Math.floor(Math.random() * img.pipeNorth.height) - img.pipeNorth.height);
    alive = population;
    //creating the birds
    var bird = [];
    for (var i = bird_begin; i <= bird_end; i++) {
        bird[i] = Bird(i);
    }
    //this function is called in every moment
    self.update = function () {
        //if there is any bird alive run, else /finishgen request is sent
        if (alive > 0) {
            ctx.drawImage(img.bg, 0, 0); //background drawing
            //shifting the pipes if neccessary
            for (var i = 0; i < pipe.length; i++) {
                if (pipe[i].pX < 0 - img.pipeNorth.width) {
                    pipe.shift();
                }
                
                constant = img.pipeNorth.height + gap;
                ctx.drawImage(img.pipeNorth, pipe[i].pX, pipe[i].pY); //North pipe drawing
                ctx.drawImage(img.pipeSouth, pipe[i].pX, pipe[i].pY + constant);//South pipe drawing
                
                ctx.drawImage(img.welcome, canvas.width/2, 0);
                
                pipe[i].update(); //updating the pipes

                if (pipe[i].pX == distance) { //new pipe
                    pipe.push(Pipe(Math.floor(Math.random() * img.pipeNorth.height) - img.pipeNorth.height));
                }

            }
            ctx.drawImage(img.fg, 0, cvs.height - img.fg.height); //foreground drawing

            //generation text
            ctx.fillStyle="blue";
            ctx.font="12px Monospace";
            ctx.textAlign = "left";
            ctx.fillText(response["generation"] + ". GENERATION", cvs.width/2 + 20, 10);

            //request[] is for /jumbird request which contains data for neural network input
            request = [];
            for (var i = bird_begin; i <= bird_end; i++) {
                if (bird[i].alive) {
                    request.push(i + '#' + parseInt(bird[i].bY) + ',' + pipe[0].pX + ',' + (pipe[0].pY + constant));
                }else{
                    request.push(i + '#' + 'dead');
                }
            }
            //drawing the birds and killing the if neccessary
            for (var i = bird_begin; i <= bird_end; i++) {
                if (bird[i].alive) {
                    ctx.drawImage(img.bird, bird[i].bX, bird[i].bY);
                    bird[i].update(gravity, command[i-bird_begin]);
                    for (var j = 0; j < pipe.length; j++) {
                        if (bird[i].bX + img.bird.width >= pipe[j].pX && bird[i].bX <= pipe[j].pX + img.pipeNorth.width && (bird[i].bY <= pipe[j].pY + img.pipeNorth.height || bird[i].bY + img.bird.height >= pipe[j].pY + constant) || bird[i].bY + img.bird.height >= cvs.height - fg.height) {
                            bird[i].kill();
                            if (fitness_scores[i] == null){
                                fitness_scores[i] = bird[i].fitness;
                            }else{
                                fitness_scores[i] += bird[i].fitness;
                            }
                            alive--;
                        }
                    }
                }

                //drawing the birds fitness scores
                var c = i - bird_begin + 1;
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
                ctx.fillText(c + ". fitness: " + bird[i].fitness, cvs.width/2 + 20, 10 + c*10);
                ctx.beginPath();
                ctx.moveTo(cvs.width/2,0);
                ctx.lineTo(cvs.width/2,cvs.height);
                ctx.stroke();
            }
            //post request for /jumpird and start update function again
            $.ajax({
                    type: "POST",
                    url: "/jumpbird",
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

        }else{//after every generation sending the /finishgen request with the fitness scores
            request = [];
            for (var i = bird_begin; i <= bird_end; i++){
                request.push(i + "#" + bird[i].fitness);
            }
            
            $.ajax({
                    type: "POST",
                    url: "/finishgen",
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

//main function for the game
var rungame =function(response){
    var game = Game(response);
    game.update();
}