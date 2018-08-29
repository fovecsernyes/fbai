var cvs = document.getElementById("canvas");
var ctx = cvs.getContext("2d");

gravity = 1.5;

var Bird = function(src)
{
    var self = new Image();
    self.bX = 10;
    self.bY = 150;
    self.src = src;
    self.fitness = 0;
    self.update = function()
    {
        self.bY += gravity;
    }
    self.moveUp = function()
    {
        self.bY -= 25;
    }
    return self;
}

var bird = new Bird("images/bird.png"); //bird

function draw() //game
{
    ctx.drawImage(bird,bird.bX,bird.bY);
    bird.update();
    requestAnimationFrame(draw); 
}

draw();