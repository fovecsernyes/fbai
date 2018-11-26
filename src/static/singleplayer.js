/// @file singleplayer.js
//  @author http://codeexplained.org
//
//  @brief This file contains "SINGLEPLAYER MODE"
//  @{

/// Setting the canvas
var cvs = document.getElementById("canvas");
var ctx = cvs.getContext("2d");


/// global variables
var bird = new Image();
var bg = new Image();
var fg = new Image();
var pipeNorth = new Image();
var pipeSouth = new Image();
var welcome = new Image();


bird.src = "/static/images/bird.png";
bg.src = "/static/images/bg.png";
pipeNorth.src = "/static/images/pipeNorth.png";
pipeSouth.src = "/static/images/pipeSouth.png";
welcome.src = "/static/images/welcome.png";


var gap = 100;
var constant;
var bX = 10;
var bY = 150;
var gravity = 1.5;
var score = 0;
var min = -256 + 250;
var max = 0;


/// Event listner when pressing key
document.addEventListener("keydown",moveUp);


/// moveUp method
function moveUp(){
    bY -= 25;
}


/// Pipes
var pipe = [];
pipe[0] = {
    x : cvs.width/2,
    y : Math.random() * (max - min) + min
};


/// Draw method
function draw(){
    ctx.drawImage(bg,0,0);
    
    for(var i = 0; i < pipe.length; i++){
        
        constant = pipeNorth.height+gap;
        ctx.drawImage(pipeNorth,pipe[i].x,pipe[i].y);
        ctx.drawImage(pipeSouth,pipe[i].x,pipe[i].y+constant);

        ctx.drawImage(welcome, canvas.width/2, 0);
             
        pipe[i].x--;
        
        if( pipe[i].x == 125 ){
            pipe.push({
                x : cvs.width/2,
                y : Math.random() * (max - min) + min
            }); 
        }

        // detect collision
        
        if( bX + bird.width >= pipe[i].x && bX <= pipe[i].x + pipeNorth.width && (bY <= pipe[i].y + pipeNorth.height || bY+bird.height >= pipe[i].y+constant) || bY + bird.height >=  cvs.height - fg.height){
            location.reload(); // reload the page
        }
        
    }

    ctx.beginPath();
    ctx.moveTo(cvs.width/2,0);
    ctx.lineTo(cvs.width/2,cvs.height);
    ctx.stroke();


    ctx.font = "12px Monospace";
    ctx.fillStyle = 'blue';
    ctx.textAlign = "left";
    ctx.fillText("Score : "+score, cvs.width/2 + 10, 30);

    ctx.font = "14px Monospace";
    ctx.fillStyle = 'white';
    ctx.textAlign = "center";
    ctx.fillText("Single player mode!", cvs.width/4*3 + 10, 90);

    ctx.font = "12px Monospace";
    ctx.fillStyle = 'black';
    ctx.textAlign = "center";
    ctx.fillText("Press any key to control the bird.", cvs.width/4*3 + 10, 120);
    ctx.fillText("Goal is to avoid the pipes.", cvs.width/4*3 + 10, 140);
    ctx.fillStyle = 'grey';
    ctx.font = "10px Monospace";
    ctx.fillText("Created by https://www.codeexplained.org", cvs.width/4*3, cvs.height - 10);


    
    ctx.drawImage(bird,bX,bY);
    
    bY += gravity;
    
    score++;
    
    requestAnimationFrame(draw);
    
}


draw();

///  @} 






















