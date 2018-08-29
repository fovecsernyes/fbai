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

var bird = new Bird("images/bird.png"); //bird
var pipeNorth = new Pipe("images/pipeNorth.png", 0);
var pipeSouth = new Pipe("images/pipeSouth.png", 400);

function draw() //game
{
    ctx.drawImage(bird, bird.bX, bird.bY);
    ctx.drawImage(pipeNorth, pipeNorth.pX, pipeNorth.pY);
    ctx.drawImage(pipeSouth, pipeSouth.pX, pipeSouth.pY);
    bird.update();
    pipeNorth.update();
    pipeSouth.update();
    requestAnimationFrame(draw); 
}

draw();