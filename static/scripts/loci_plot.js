
var elt = document.getElementById('calculator');
var options = {
    expressions:true,
    expressionsCollapsed:true,
    keypad:false,
    settingsMenu:false
}
var calculator = Desmos.Calculator(elt,options);
calculator.setGraphSettings({xAxisLabel:'Re',yAxisLabel:'Im'})
var reset = calculator.getState();

var plots = -1

function addplot(){
var eq = $('input[name="in"]').val()
$.getJSON($SCRIPT_ROOT + '/_plot', {
    eq: eq
}, function(data) {
    plots += 1;
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

}).fail(function(){
    $('#eq_in').blur()
    alert('Please enter a valid equation')
    $('#eq_in').focus()
});
return false;

}


$(document).ready(function() {
    $('#eq_in').on('keydown', function(e) {
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
    $('#submit-graph').on('click',function(){
        exprlist = $('#expressions td:nth-child(1)').map(function(){
            return $(this).text(); //need to get from mathjax, not just text
        }).get();
        //TODO exprlist not working, implement JSON object as {id:plot}
        $.post('/_addgraph',{
            title:$('#title').val(),
            desmosdata:JSON.stringify(calculator.getState()),
            exprlist:$('#expressions').html(),
            description:$('#desc').val()
        },function(data){
            if (data.status === 'ok') {
                $('#save-modal').modal('hide')
                alert("Successfully saved graph")
                html='<option value='+data.id+'>'+data.title+'</option>'
                $('#graph-select').append($('<option>',{value:data.id,text:data.title}))
            } else {
                alert(data.error)
                $('#eq_in').focus()
            }
            });
    });
    $('#load-graph').on('click',function(){
        console.log($("#graph-select").val())
        id = $("#graph-select").val()
        $.getJSON($SCRIPT_ROOT+'/_addgraph',{
            graph_id: id
        },function(data){
            $('#load-modal').modal('hide')
            $('#expressions').html(data.exprlist)
            calculator.setState(data.desmosdata)
        }).fail(function(){
            alert('Error Loading Graph')
        });
    })
    //modal made in jinja at start, then graphs added into html when one is saved
});
