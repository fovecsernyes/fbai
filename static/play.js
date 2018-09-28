function dropdown(begin, end, add){
    var options = "";
    for(var i=begin; i<=end; i=i+add){
        options += "<option>"+ i +"</option>";
    }
    return options;
}

function start_gen(){
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

var Bird = function () {
    var self = {
        bX: 10,
        bY: 150,
        fitness: 0,
        alive: true
    }

    self.update = function (gravity) {
        self.fitness++;
        self.bY += gravity;
        if (Math.floor(18 * Math.random()) % 18 === 0) {
            self.moveUp();
        }
    }

    self.moveUp = function () {
        self.bY -= 25;
    }

    self.kill = function () {
        self.alive = false;
    }

    return self;
}

var Pipe = function (y) {
    var self =
    {
        pX: cvs.width/2,
        pY: y
    }

    self.update = function () {
        self.pX--;
    }
    return self;
}

var Game = function (response) {
    var gravity = parseInt(response["gravity"])/5;
    var population = parseInt(response["population"]);
    var gap = parseInt(response["gap"]);
    var distance = 288 - parseInt(response["distance"]);

    var img = LoadImages();

    var pipe = [];
    pipe[0] = Pipe(0);
    alive = population;

    var bird = [];
    for (var i = 0; i < population; i++) {
        bird[i] = Bird();
    }

    self.update = function () {
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
                pipe.push(Pipe(Math.floor(Math.random() * img.pipeNorth.height) - img.pipeNorth.height));
            }

        }
        ctx.drawImage(img.fg, 0, cvs.height - img.fg.height);

        ctx.fillStyle="blue";
        ctx.font="12px Monospace";
        ctx.textAlign = "left";
        ctx.fillText(response["generation"] + ". GENERATION", cvs.width/2 + 20, 10);

        for (var i = 0; i < bird.length; i++) {
            if (bird[i].alive) {
                ctx.drawImage(img.bird, bird[i].bX, bird[i].bY);
                bird[i].update(gravity);
                for (var j = 0; j < pipe.length; j++) {
                    if (bird[i].bX + img.bird.width >= pipe[j].pX && bird[i].bX <= pipe[j].pX + img.pipeNorth.width && (bird[i].bY <= pipe[j].pY + img.pipeNorth.height || bird[i].bY + img.bird.height >= pipe[j].pY + constant) || bird[i].bY + img.bird.height >= cvs.height - fg.height) {
                        bird[i].kill();
                        alive--;
                    }
                }
            }
            var c = i + 1;
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
            ctx.fillText(c + ". fitness: " + bird[i].fitness, cvs.width/2 + 20, 20 + i*10);
            ctx.beginPath();
            ctx.moveTo(cvs.width/2,0);
            ctx.lineTo(cvs.width/2,cvs.height);
            ctx.stroke();
        }
        if (alive > 0) {
            requestAnimationFrame(update);
        }else{
            $.ajax({
                    type: "POST",
                    url: "/finishgen",
                    contentType: "application/json",
                    data: JSON.stringify( {"request" : "finishgen"} ),
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

function rungame(response){
    var game = Game(response);
    game.update();
}