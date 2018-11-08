/// @file aiplayer.js
//  @author Mark Vecsernyes
//
//  @brief Ez a fájl tartalmazza az "AIPLAYER MODE"-ot
//  @{

/// A legördülő listamező megmutatása
var show_label = function(){
    label[0] =  $('#gra_dd').val();
    label[1] = $('#jum_dd').val();
    label[2] = $('#pop_dd').val();
    label[3] = $('#gap_dd').val();
    label[4] = $('#dis_dd').val();
        
    label[5] = $('#hid_dd').val();
    label[6] = $('#sel_dd').val();
    label[7] = $('#del_dd').val();
    label[8] = $('#cro_dd').val();
    label[9] = $('#mu1_dd').val();
    label[10] = $('#mu2_dd').val();

    $('#gra_dd').val("Gravity");
    $('#jum_dd').val("Jump");
    $('#pop_dd').val("Population");
    $('#gap_dd').val("Gap");
    $('#dis_dd').val("Distance");

    $('#hid_dd').val("Hidden neurons");
    $('#sel_dd').val("Selection rates");
    $('#del_dd').val("Deletion rate");
    $('#cro_dd').val("Crossover rate");
    $('#mu1_dd').val("Mutation rate on population");
    $('#mu2_dd').val("Mutation rate on entity");

}

var hide_label = function(){
    $('#gra_dd').val(label[0]);
    $('#jum_dd').val(label[1]);
    $('#pop_dd').val(label[2]);
    $('#gap_dd').val(label[3]);
    $('#dis_dd').val(label[4]);

    $('#hid_dd').val(label[5]);
    $('#sel_dd').val(label[6]);
    $('#del_dd').val(label[7]);
    $('#cro_dd').val(label[8]);
    $('#mu1_dd').val(label[9]);
    $('#mu2_dd').val(label[10]);
}

/// A legördülő listamező létrehozása
//  @param begin integer a lita eleje
//  @param end integer a lsita vége
//  @param add integer hányasával lépkedjen a lista
//  @param label string a lista felirata
//  @return optrions string a lista maga
var dropdown = function(begin, end, add, label){
    options = "<option disabled>" + label + "</option>";
    for(var i=begin; i<=end; i=i+add){
        options += "<option>"+ i +"</option>";
    }
    return options;
}

/// Minden generáció elején a /ai/startgen címre küldő POST kérés
//  a rungame metódust hívja meg válasz után
var start_gen = function(){
        $.ajax({
            type: "POST",
            url: "/ai/startgen",
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

/// Képek betöltése metódus
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

/// Madarakatat leíró osztály
//  @param db_id string a madarak azonosítói
var Bird = function (db_id) {
    var self = {
        bX: 10,
        bY: 150,
        id: db_id,
        fitness: 0,
        alive: true
    }
    /// A madarak frissítése
    //  @param gravity integer a gravitáció értéke
    //  @param command integer 0 - semmi, 1 - ugorjon
    //  @param jump intgere az ugrás magassága
    self.update = function (gravity, command, jump) {
        self.fitness++;
        self.bY += gravity;
        if(command){
            self.moveUp(jump);
        }
    }
    /// Madár felfelé mozgása
    //  @param jump az ugrás magassága
    self.moveUp = function (jump) {
        self.bY -= jump;
    }

    return self;
}

/// Oszlopokat leíró osztály
//  @param y integer az oszlop közepének koordinátája
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

/// Játékok leíró osztály
//  @param response running_params 
var Game = function (response) {
    //variables mainly from backend response
    var fitness_scores = [];
    var gravity = response["gravity"]/5;
    var population = response["population"];
    var gap = response["gap"];
    var jump = response["jump"];
    var distance = 288 - response["distance"];
    var birds_ids = JSON.parse(response["bird_ids"]);
    var bird_begin = parseInt(birds_ids[0]);
    var bird_end = parseInt(birds_ids[population-1]);
    var command = new Array(population).join(0).split('');

    var img = LoadImages();

    var pipe = [];
    pipe[0] = Pipe(Math.floor(Math.random() * img.pipeNorth.height) - img.pipeNorth.height);
    alive = population;

    var bird = [];
    for (var i = bird_begin; i <= bird_end; i++) {
        bird[i] = Bird(i);
    }
    /// Játék frissítése metódus
    //  minden időpillanatban küld egy POST kérést a /ai/jumpbird címre a madarak pozíciójával majd újra lefut
    //  ha minden madár meghal akkor elküldi a fitness értékeket 
    self.update = function () {
        if (alive > 0) {
            alive = 0;
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

            request = [];
            for (var i = bird_begin; i <= bird_end; i++) {
                if (bird[i].alive) {
                    request.push(i + '#' + parseInt(bird[i].bY) + ',' + pipe[0].pX + ',' + (pipe[0].pY + constant));
                }else{
                    request.push(i + '#' + 'dead');
                }
            }
            for (var i = bird_begin; i <= bird_end; i++) {
                if (bird[i].alive) {
                    bird[i].update(gravity, command[i-bird_begin], jump);
                    ctx.drawImage(img.bird, bird[i].bX, bird[i].bY);
                    for (var j = 0; j < pipe.length; j++) {
                        if (bird[i].bX + img.bird.width >= pipe[j].pX && bird[i].bX <= pipe[j].pX + img.pipeNorth.width && (bird[i].bY <= pipe[j].pY + img.pipeNorth.height || bird[i].bY + img.bird.height >= pipe[j].pY + constant) || bird[i].bY + img.bird.height >= cvs.height - fg.height) {
                            bird[i].alive = false;
                            if (fitness_scores[i] == null){
                                fitness_scores[i] = bird[i].fitness;
                            }else{
                                fitness_scores[i] += bird[i].fitness;
                            }
                        }
                    }
                }
                if(bird[i].alive){
                    alive++;
                }
                var c = i - bird_begin;
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
                if( (i - bird_begin + 1) <= 50 ){
                    ctx.fillText(c + ". fitness: " + bird[i].fitness, cvs.width/2 + 20, 20 + c*10);
                }else{
                    ctx.fillText(c + ". fitness: " + bird[i].fitness, cvs.width/2 + 170, 20 + (c-50)*10);
                }

                ctx.beginPath();
                ctx.moveTo(cvs.width/2,0);
                ctx.lineTo(cvs.width/2,cvs.height);
                ctx.stroke();
            }

            $.ajax({
                    type: "POST",
                    url: "/ai/jumpbird",
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

        }else{
            request = [];
            for (var i = bird_begin; i <= bird_end; i++){
                request.push(i + "#" + bird[i].fitness);
            }
            
            $.ajax({
                    type: "POST",
                    url: "/ai/finishgen",
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

/// Játék futtatása
var rungame =function(response){
    var game = Game(response);
    game.update();
}

/// @}