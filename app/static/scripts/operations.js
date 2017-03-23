// Get width and height of box in pixels
var w = $('#box').width();
var h = $('#box').height();
// Make sure the axes have the same scale
var x_ax=w/20;
var y_ax=h/20;
var board_atts = {
        boundingbox: [-x_ax, y_ax, x_ax, -y_ax],
        axis: true,
        showCopyright:false,
        showNavigation:false,
        pan: {
            enabled: true,
            needshift: false,
            needTwoFingers: true
        },
        zoom: {
            factorX: 1.25,
            factorY: 1.25,
            wheel: true,
            needshift: false
        }
}
// Initialize board
board = JXG.JSXGraph.initBoard('box',board_atts);
// Create hidden origin point
var org = board.create('point', [0,0], {style:10,visible:false,fixed:true,name:' '});
// Initialise points and lines objects, and start letter at 'a'
var points = {};
var org_lines = {}
var letter = 'a';

$(document).ready(function(){
    $('#addpoint').on('click',function(){
        // Function for adding a new moveable point
        //  Increment letter
        letter = String.fromCharCode(letter.charCodeAt()+1);
        // Add new points at (1,1)
        points[letter] = board.create('point',[1,1],{style:4,color:'red',strokeColor:'red',name:letter});
        // Add line from origin to point
        org_lines[letter] = board.create('arrow',[org,points[letter]],{strokeColor:'blue'})
        // Add row to table
        $('#expressions tbody').append('<tr id="row'+letter+'">'+
            '<td><b>'+letter+'</b></td>'+
            '<td>'+
                '<input id="re'+letter+'" style="width:50px" value="'+points[letter].X().toFixed(2)+'">+'+
                '</td><td><input id="im'+letter+'" style="width:50px" value="'+points[letter].Y().toFixed(2)+'">i'+
            '</td>'+
            '<td>'+
                '<input type="checkbox" name="plot" id="show'+letter+'" checked>'+
            '</td>'+
            '<td>'+
                '<input type="checkbox" name="plot" id="line'+letter+'" checked>'+
            '</td>'+
            '<td>'+
                '<input type="button" class="btn btn-block" name="del" id="del'+letter+'" value="X">'+
            '</td>'+
        '</tr>');
    });
    $('#addcalc').on('click',function(){
        // Function for adding calculated point
        // Get form input
        calc = $('#calc_in').val()
        // Send data to server as GET request at /_addcalc
        $.getJSON($SCRIPT_ROOT + '/_addcalc',{
            eq:calc,
        }, function(data){ // Function for recieved data
            // Increment letter
            letter = String.fromCharCode(letter.charCodeAt()+1);
            // Add points with coordinates from recieved data
            points[letter] = board.create('point',[data.x,data.y],{style:4,color:'blue',strokeColor:'blue',name:letter});
            // Add line from origin to point
            org_lines[letter] = board.create('arrow',[org,points[letter]],{strokeColor:'red'})
            // Add row to table
            $('#expressions tbody').append('<tr id="row'+letter+'">'+
                '<td><b>'+letter+'</b></td>'+
                '<td colspan="2" id="label'+letter+'">'+
                    '`'+points[letter].X().toFixed(2)+'+'+points[letter].Y().toFixed(2)+'i'+'`'+
                '</td>'+
                '<td>'+
                    '<input type="checkbox" name="plot" id="show'+letter+'" checked>'+
                '</td>'+
                '<td>'+
                    '<input type="checkbox" name="plot" id="line'+letter+'" checked>'+
                '</td>'+
                '<td>'+
                    '<input type="button" class="btn btn-block" name="del" id="del'+letter+'" value="X">'+
                '</td>'+
            '</tr>');
        }).fail(function(){
            // Error message if there if function fails
            alert('Invalid calculation')
        });
    });
    $('#box').on('click change mouseup mousedown',function(){
        // When box is clicked, update the table which displays the points
        // The box being clicked means a points is moved
        console.log('aa');
        for (var letter in points) {
            // get x and y of all points

            var x = parseFloat(points[letter].X())
            var y = parseFloat(points[letter].Y())
            console.log(x,y)
            if ($('#label'+letter).length>0) {
                // Change table cell of calculated points
                $('#label'+letter).html(x.toFixed(2)+'+'+y.toFixed(2)+'i')
            } else {
                // Change value of inputs for moveable points
                $('#re'+letter).val(x.toFixed(2))
                $('#im'+letter).val(y.toFixed(2))
            }
        }
    });
    $('#clear').on('click', function() {
        // Delete table
        $('#expressions tbody > tr').remove();
        // Reset variables and recreate board
        points = {}
        lines = {}
        letter = 'a'
        JXG.JSXGraph.freeBoard(board);
        board = JXG.JSXGraph.initBoard('box', board_atts);
    });
    $('#expressions').on('click','[type=button]',function(){
        // Get id of button clicked, and get letter which it corresponds to
        var id = $(this).attr('id').replace('del','');
        // Remove point with the id
        board.removeObject(points[id]);
        // delete from points object
        delete points[id];
        // remove row from table
        $('#row'+id).remove();
    });
    $('#expressions').on('click','[type=checkbox][id*=show]',function(){
        // Get id of checkbox clicked, and get letter which it corresponds to
        var id=$(this).attr('id').replace('show','')
        // See whether point is visible
        point_vis = points[id].getAttribute('visible');
        // Flip visibility of point and corresponding line
        points[id].setAttribute({visible:!point_vis})
        org_lines[id].setAttribute({visible:!point_vis})
    });
    $('#expressions').on('click','[type=checkbox][id*=line]',function(){
        // Get id of checkbox clicked, and get letter which it corresponds to
        var id=$(this).attr('id').replace('line','')
        // See whether line is visible or not
        vis = org_lines[id].getAttribute('visible');
        // Flip hidden attribute
        org_lines[id].setAttribute({visible:!vis})
    });
    $('#expressions').on('keyup',function(){
        for (var letter in points) {
            if ($('#re'+letter).length>0){
                points[letter].setPosition(JXG.COORDS_BY_USER,[parseFloat($('#re'+letter).val()),parseFloat($('#im'+letter).val())])
            }
        }
        board.fullUpdate()
    });
});
