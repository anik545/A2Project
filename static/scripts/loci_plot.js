
var elt = document.getElementById('calculator');
var options = {
    expressions:true,
    expressionsCollapsed:true,
    keypad:false,
    settingsMenu:false
}
var calculator = Desmos.Calculator(elt,options);
var reset = calculator.getState();

var w = $('#calculator').width();
var h = $('#calculator').height();
var x_ax=w/20;
var y_ax=h/20;

var plots = -1

function addplot(){
var eq = $('input[name="in"]').val()
$.getJSON($SCRIPT_ROOT + '/_plot', {
    eq: eq
}, function(data) {
    plots += 1;
    //TODO check if i is in string, an draise error if it is --> dont plot
    $('#expressions tbody').append(
        '<tr id="row'+plots+'">'+
            '<td>'+
                '`'+eq+'`'+
            '</td>'+
            '<td>'+
                '<input type="checkbox" name="plot" id="'+plots+'" checked>'+
            '</td>'+
            '<td>'+
                '<input type="button" class="btn btn-block" name="del" id="del'+plots+'" value="X">'+
            '</td>'+
        '</tr>'
    );

    MathJax.Hub.Queue(["Typeset",MathJax.Hub,"expressions"]);

    var result = data.result;
    console.log(result)
    calculator.setExpression({id:plots,latex:result});

});
return false;

}


$(document).ready(function() {
    $('#eq_in').on('keyup', function(e) {
        if (e.keyCode===13) {
            addplot();
        }});
    $('#go').on('click', addplot);
    $('#clear').on('click', function() {
        $('#expressions tbody > tr').remove();
        plots = -1;
        calculator.setState(reset);
        //Clear All
    });
    $('#expressions').on('click','[type=button]',function(){
        var plot_no = $(this).attr('id').replace('del','');
        $('#row'+plot_no).remove();
        calculator.removeExpression({id:parseInt(plot_no)})
    });
    $('#expressions').on('click','[type=checkbox]',function(){
        var plot_no=$(this).attr('id')
        var vis = $(this).is(':checked')
        calculator.setExpression({id:plot_no,hidden:!vis})
        // Show/Hide line(s)
    });

});
