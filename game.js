var cvs = document.getElementById("canvas");
var ctx = cvs.getContext("2d");

var gravity = 1.5; //userinput
var population = 150; //userinput
var gap = 85; //user input

var LoadImages = function () {
    bg = new Image();
    fg = new Image();

    bg.src = "images/bg.png";
    fg.src = "images/fg.png";

    bird = new Image();
    pipeNorth = new Image();
    pipeSouth = new Image();
    bird.src = "images/bird.png";
    pipeNorth.src = "images/pipeNorth.png";
    pipeSouth.src = "images/pipeSouth.png";

    return self;
}

var Bird = function () {
    var self = {
        bX: 10,
        bY: 150,
        //angle: 0,
        fitness: 0,
        alive: true
    }

    self.update = function () {
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
        pX: cvs.width,
        pY: y
    }

    self.update = function () {
        self.pX--;
    }
    return self;
}

var Game = function () {
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
            pipe[i].update();

            if (pipe[i].pX == 125) {
                pipe.push(Pipe(Math.floor(Math.random() * img.pipeNorth.height) - img.pipeNorth.height));
            }

        }

        ctx.drawImage(img.fg, 0, cvs.height - img.fg.height);

        for (var i = 0; i < bird.length; i++) {
            if (bird[i].alive) {
                ctx.drawImage(img.bird, bird[i].bX, bird[i].bY);
                bird[i].update();
                for (var j = 0; j < pipe.length; j++) {
                    if (bird[i].bX + img.bird.width >= pipe[j].pX && bird[i].bX <= pipe[j].pX + img.pipeNorth.width && (bird[i].bY <= pipe[j].pY + img.pipeNorth.height || bird[i].bY + img.bird.height >= pipe[j].pY + constant) || bird[i].bY + img.bird.height >= cvs.height - fg.height) {
                        bird[i].kill();
                        alive--;
                    }
                }
            }
        }
        //sometimes goes under 0 (tried with #180 birds)
        if (alive == 0) {
            location.reload();
        }

        requestAnimationFrame(update);
    }
    return self;
}

var game = Game();
game.update();