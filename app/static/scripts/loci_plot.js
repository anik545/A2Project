
var elt = document.getElementById('calculator');
// Options for desmos grpah plotter
var options = {
    expressions:true,
    expressionsCollapsed:true,
    keypad:false,
    settingsMenu:false
}
// Initialize plotter
var calculator = Desmos.Calculator(elt,options);
calculator.setGraphSettings({xAxisLabel:'Re',yAxisLabel:'Im'})
// Create reset state (for when the user resets the plotter)
var reset = calculator.getState();

var plots = -1

function addplot(){
// Get input from equation input field
var eq = $('input[name="in"]').val()
// Send GET request to server at /_plot with 'eq' variable
$.getJSON($SCRIPT_ROOT + '/_plot', {
    eq: eq
}, function(data) {  //function carried out on receiving data from server
    // Increment plots counter
    // Allows each plot to have an unique id
    plots += 1;
    // Add html for a row in the expressions table
    // Includes the expression, show/hide checkbox, delete button
    $('#expressions tbody').append(
        '<tr id="row'+plots+'">'+
            '<td>'+
                '`'+data.eq+'`'+
            '</td>'+
            '<td>'+
                '<input type="checkbox" name="plot" id="'+plots+'" checked>'+
            '</td>'+
            '<td>'+
                '<input type="button" class="btn btn-block" name="del" id="del'+plots+'" value="X">'+
            '</td>'+
        '</tr>'
    );
    // Typeset math
    MathJax.Hub.Queue(["Typeset",MathJax.Hub,"expressions"]);
    // Get result from received data
    var result = data.result;
    console.log(result)
    // Add expression to desmos plot
    calculator.setExpression({id:plots,latex:result});

}).fail(function(){  //Display error message if server returns an error
    $('#eq_in').blur()
    alert('Please enter a valid equation')
    $('#eq_in').focus()
});
return false;
}


$(document).ready(function() {
    $('#graph-select').imagepicker({show_label:true})
    var queryDict = {};
    // Get all parameters
    location.search.substr(1).split("&").forEach(function(item) {queryDict[item.split("=")[0]] = item.split("=")[1]});
    // If there is an id parameter, load graph with that id
    if (queryDict['id']) {
        $.getJSON($SCRIPT_ROOT+'/_addgraph',{
            graph_id: queryDict['id']
        },function(data){
            $('#load-modal').modal('hide')
            $('#expressions').html(data.exprlist)
            calculator.setState(data.desmosdata)
        }).fail(function(){
            alert('Error Loading Graph')
        });
    }
    // If enter pressed while in the input box, add the plot to the graph
    $('#eq_in').on('keydown', function(e) {
        if (e.keyCode===13) {
            addplot();
        }});
    // CLicking the go button also adds a plot to the graph
    $('#go').on('click', addplot);
    // Function for clear all button
    $('#clear').on('click', function() {
        // Delete all rows in expressions table
        $('#expressions tbody > tr').remove();
        // Reset plot counter
        plots = -1;
        // Reset calculator
        calculator.setState(reset);
    });
    // Button for deleting individual plots
    $('#expressions').on('click','[type=button]',function(){
        // Get the id of button that was clicked - corresponds to the plots id
        var plot_no = $(this).attr('id').replace('del','');
        // Delete relevant row in expressions table
        $('#row'+plot_no).remove();
        // Delete relevant plot on graph
        calculator.removeExpression({id:parseInt(plot_no)})
    });
    // Show/hide line(s)
    $('#expressions').on('click','[type=checkbox]',function(){
        // Get id of checkbox clicked
        var plot_no=$(this).attr('id')
        // See whether the checkbox is checked or not
        var checked = $(this).is(':checked')
        // Set hidden attribute of the expression the opposite of checked
        calculator.setExpression({id:plot_no,hidden:!checked})
    });
    // Function for saving a graph
    $('#submit-graph').on('click',function(){
        // Send POST request to server at '/_addgraph' with data:
        // Graph title, graph data from desmos, the html for the expressions table,
        // Graph description, image data from a screenshot of graph
        $.post('/_addgraph',{
            title:$('#title').val(),
            desmosdata:JSON.stringify(calculator.getState()),
            exprlist:$('#expressions').html(),
            description:$('#desc').val(),
            image: calculator.screenshot({width:100,height:100,targetPixelRatio:2})
        },function(data){
            if (data.status === 'ok') {
                // If there was no error
                // Hide the save-graph dialog
                $('#save-modal').modal('hide')
                // Add option to load-graph dialog
                $('#graph-select').append('<option value="'+data.id+'" data-img-src="'+data.image_url+'">'+data.title+'</option>')
                alert("Successfully saved graph")
                $('#graph-select').imagepicker({show_label:true})
            } else {
                // If there was an error, display the error message in a pop-up
                alert(data.error)
                $('#eq_in').focus()
            }
            });
    });
    // Function for loading a saved graph
    $('#load-graph').on('click',function(){
        console.log($("#graph-select").val())
        // Get the id of the graph selected
        id = $("#graph-select").val()
        // Send GET request to server with graph_id
        $.getJSON($SCRIPT_ROOT+'/_addgraph',{
            graph_id: id
        },function(data){  //Function carried out when data recieved
            // Hide the load-graph modal is not already hidden
            $('#load-modal').modal('hide')
            // Put exressions data into the table (from recieved data)
            $('#expressions').html(data.exprlist)
            // Set the calculator state
            calculator.setState(data.desmosdata)
        }).fail(function(){
            // Display error message on server error
            alert('Error Loading Graph')
        });
    })
    //modal made in jinja at start, then graphs added into html when one is saved
});
