var cvs = document.getElementById("canvas");
var ctx = cvs.getContext("2d");

gravity = 1.5; //userinput
population = 5; //userinput

//bird class
var Bird = function(src)
{
    var self = new Image();
    self.bX = 10;
    self.bY = 150;
    self.angle = 0;
    self.src = src;
    self.fitness = 0;
    self.alive = true;

    self.update = function()
    {
        self.bY += gravity;
        if(Math.floor(30 * Math.random()) % 30 === 0){
            self.moveUp();
        }
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
    bg = Environment("images/bg.png");
    fg = Environment("images/fg.png");

    var birds = new Array(population);
    for (var i = 0; i < population; i++ )
    {
        birds[i] = Bird("images/bird.png");
    }   

    pipeNorth = Pipe("images/pipeNorth.png", 0);
    pipeSouth = Pipe("images/pipeSouth.png", 400);

    self.update = function()
    {
        ctx.drawImage(bg,0,0);
        ctx.drawImage(fg,0,cvs.height - fg.height);
        ctx.drawImage(pipeNorth, pipeNorth.pX, pipeNorth.pY);
        ctx.drawImage(pipeSouth, pipeSouth.pX, pipeSouth.pY);
        pipeNorth.update();
        pipeSouth.update();

        for (var i = 0; i < population; i++)
        {
            ctx.drawImage(birds[i], birds[i].bX, birds[i].bY);
            birds[i].update();
        }
        
        requestAnimationFrame(update); 
    }
    return self;
}

var game = Game();
game.update();