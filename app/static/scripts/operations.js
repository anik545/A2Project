board = JXG.JSXGraph.initBoard('box', {boundingbox: [-6, 6, 8, -4], axis: true});

var org = board.create('point', [0,0], {style:10,visible:true,fixed:true,name:' '});
var x = board.create('point', [2,2], {style:5,color:'blue',name:'x'});
var y = board.create('point', [-1,-3], {style:5,color:'blue',name:'y'});
var xy = board.create('point',
    ["X(x)+X(y)","Y(x)+Y(y)"], {style:7,color:'green',name:'x+y'});
var ax =board.create('arrow', [org,x], {strokeColor:'blue'});
var ay =board.create('arrow', [org,y], {strokeColor:'blue'});
var axy =board.create('arrow', [org,xy], {strokeColor:'red'});
var ax2 =board.create('arrow', [x,xy], {strokeColor:'blue',strokeWidth:1,dash:1});
var ay2 =board.create('arrow', [y,xy], {strokeColor:'blue',strokeWidth:1,dash:1});

//brd2 = JXG.JSXGraph.initBoard('box2', {boundingbox: [-6, 6, 8, -4], axis: true});

var org2 = board.create('point', [0,0], {style:10,visible:true,fixed:true,name:' '});
var x2 = board.create('point', [1,0], {style:4,color:'blue',name:'x'});
var y2 = board.create('point', [0,2], {style:4,color:'red',strokeColor:'red',name:'y'});
var xy2 = board.create('point',
    ["X(x)*X(y)-Y(x)*Y(y)","X(x)*Y(y)+X(y)*Y(x)"], {style:7,fillColor:'green',strokeColor:'green',name:'x*y'});
var c = board.create('circle',[org2,1],{strokeWidth:1,dash:1});

var points = {};
var letter = 'a';

$(document).ready(function(){
    $('#addpoint').on('click',function(){
        letter = String.fromCharCode(letter.charCodeAt()+1);
        points[letter] = board.create('point',[1,1],{style:4,color:'red',strokeColor:'red',name:letter});
        $('#expressions tbody').append(
                '<tr id="row'+letter+'">'+
                    '<td id="label'+letter+'">'+
                        '`'+points[letter].X()+'+'+points[letter].Y()+'i'+'`'+
                    '</td>'+
                    '<td>'+
                        '<input type="checkbox" name="plot" id="'+letter+'" checked>'+
                    '</td>'+
                    '<td>'+
                        '<input type="button" class="btn btn-block" name="del" id="del'+letter+'" value="X">'+
                    '</td>'+
                '</tr>'
            );
        points[letter].on('up',function(){
            console.log('aa')
            $('#label'+letter).html('`'+points[letter].X()+'+'+points[letter].Y()+'`')
        });
    });
});
