var cvs = document.getElementById("canvas");
var ctx = cvs.getContext("2d");

gravity = 1.5; //userinput

//bird class
var Bird = function(src)
{
    var self = new Image();
    self.bX = 10;
    self.bY = 150;
    self.src = src;
    self.fitness = 0;
    self.alive = true;

    self.update = function()
    {
        self.bY += gravity;
    }

    self.moveUp = function()
    {
        self.bY -= 25;
    }

    self.kill = function()
    {
        self.alive = false;
    }

    return self;
}

var Pipe = function(src, gap)
{
    var self = new Image();
    self.src = src;
    self.pX = cvs.width;
    self.pY = gap;

    self.update = function()
    {
        self.pX--;
    }
    return self;
}

var Environment = function(src)
{
    var self = new Image();
    self.src = src;
    return self;
}

var Game = function()
{
    bg = new Environment("images/bg.png");
    fg = new Environment("images/fg.png");
    bird = new Bird("images/bird.png");
    pipeNorth = new Pipe("images/pipeNorth.png", 0);
    pipeSouth = new Pipe("images/pipeSouth.png", 400);

    self.update = function()
    {
        ctx.drawImage(bg,0,0);
        ctx.drawImage(fg,0,cvs.height - fg.height);
        ctx.drawImage(pipeNorth, pipeNorth.pX, pipeNorth.pY);
        ctx.drawImage(pipeSouth, pipeSouth.pX, pipeSouth.pY);
        ctx.drawImage(bird, bird.bX, bird.bY);
        pipeNorth.update();
        pipeSouth.update();
        bird.update();
        requestAnimationFrame(update); 
    }
    return self;
}

var game = Game();
game.update();