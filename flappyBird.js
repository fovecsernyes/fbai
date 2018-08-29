//var cvs = document.getElementById("canvas");
//var ctx = cvs.getContext("2d");

// load images

//var bird = new Image(); //bird
//var bg = new Image(); //game
//var fg = new Image(); //game
//var pipeNorth = new Image(); //pipe
//var pipeSouth = new Image(); //pipe

//bird.src = "images/bird.png"; //bird
//bg.src = "images/bg.png"; //game
//fg.src = "images/fg.png"; //game
//pipeNorth.src = "images/pipeNorth.png"; //pipe
//pipeSouth.src = "images/pipeNorth.png"; //pipe


// some variables

var gap = 85; //pipe
var constant; //?

//var bX = 10; //bird
//var bY = 150; //bird

//var gravity = 1.5; //environment

//var score = 0; //bird

// audio files

//var fly = new Audio(); //no need
//var scor = new Audio(); //no need 

//fly.src = "sounds/fly.mp3"; //no need
//scor.src = "sounds/score.mp3";//no need

// on key down

//document.addEventListener("keydown",moveUp); //no need

//function moveUp(){ //bird
//    bY -= 25;
//    fly.play();
//}

// pipe coordinates

var pipe = []; //game

pipe[0] = { //game
    x : cvs.width,
    y : 0
};

// draw images

function draw(){ //game
    
    ctx.drawImage(bg,0,0);
    
    
    for(var i = 0; i < pipe.length; i++){
        
        constant = pipeNorth.height+gap;
        ctx.drawImage(pipeNorth,pipe[i].x,pipe[i].y);
        ctx.drawImage(pipeSouth,pipe[i].x,pipe[i].y+constant);
             
        pipe[i].x--;
        
        if( pipe[i].x == 125 ){
            pipe.push({
                x : cvs.width,
                y : Math.floor(Math.random()*pipeNorth.height)-pipeNorth.height
            }); 
        }

        // detect collision
        
        if( bX + bird.width >= pipe[i].x && bX <= pipe[i].x + pipeNorth.width && (bY <= pipe[i].y + pipeNorth.height || bY+bird.height >= pipe[i].y+constant) || bY + bird.height >=  cvs.height - fg.height){
            location.reload(); // reload the page
        }
        
        if(pipe[i].x == 5){
            score++;
            scor.play();
        }
        
        
    }

    ctx.drawImage(fg,0,cvs.height - fg.height);
    
    ctx.drawImage(bird,bX,bY);
    
    bY += gravity;
    
    ctx.fillStyle = "#000";
    ctx.font = "20px Verdana";
    ctx.fillText("Score : "+score,10,cvs.height-20);
    
    requestAnimationFrame(draw);
    
}

draw();
























