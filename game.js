var cvs = document.getElementById("canvas");
var ctx = cvs.getContext("2d");

var gravity = 1.5; //userinput
var population = 5; //userinput
var gap = 85; //user input

bg = new Image();
fg = new Image();

bg.src = "images/bg.png";
fg.src = "images/fg.png";

birdImg = new Image();
pipeNorthImg = new Image();
pipeSouthImg = new Image();
birdImg.src = "images/bird.png";
pipeNorthImg.src = "images/pipeNorth.png";
pipeSouthImg.src = "images/pipeSouth.png";

//bird class
var Bird = function()
{
    var self = 
    {
        bX: 10,
        bY: 150,
        //angle: 0,
        fitness: 0,
        alive: true
    }

    self.update = function()
    {
        self.bY += gravity;
        if(Math.floor(18 * Math.random()) % 18 === 0){
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

var Pipe = function(y)
{
    var self = 
    {
        pX: cvs.width,
        pY: y
    }

    self.update = function()
    {
        self.pX--;
    }
    return self;
}

var Game = function()
{
    var pipe = [];
    pipe[0] = Pipe(0);

    var bird = [];
    for (var i = 0; i < population; i++ )
    {
        bird[i] = Bird();
    }   

    self.update = function()
    {
        ctx.drawImage(bg,0,0);
        for(var i = 0; i < pipe.length; i++)
        {
            if(pipe[i].pX <  0 - pipeNorthImg.width)
            {
                pipe.shift();
            }

            constant = pipeNorthImg.height+gap;
            ctx.drawImage(pipeNorthImg, pipe[i].pX, pipe[i].pY);
            ctx.drawImage(pipeSouthImg, pipe[i].pX, pipe[i].pY+constant);
            pipe[i].update();

            if( pipe[i].pX == 125 )
            {
                pipe.push(Pipe(Math.floor(Math.random()*pipeNorthImg.height)-pipeNorthImg.height)); 
            }

        }

        ctx.drawImage(fg,0,cvs.height - fg.height);

        for (var i = 0; i < bird.length; i++)
        {
 

            if (bird[i].alive)
            {
                ctx.drawImage(birdImg, bird[i].bX, bird[i].bY);
                bird[i].update();
                // for (var i = 0; i < pipe.length; i++)
                // {
                //     if( bird[i].bX + birdImg.width >= pipe[i].pX && bird[i].bX <= pipe[i].pX + pipeNorthImg.width && (bird[i].bY <= pipe[i].pY + pipeNorthImg.height || bird[i].bY+birdImg.height >= pipe[i].pY+constant) || bird[i].bY + birdImg.height >=  cvs.height - fg.height)
                //     {
                //     bird[i].kill();
                //     } 
                // }
            }
        }

        requestAnimationFrame(update); 
    }
    return self;
}

var game = Game();
game.update();