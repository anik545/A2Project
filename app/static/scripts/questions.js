$('#submit').on('click', function() {
    // When submit clicked, run function submit_answers
    submit_answers()
});

function submit_answers() {
    // Get data from questions form as a dictionary
    var data = $('#questions').serializeArray().reduce(function(obj, item) {
        obj[item.name] = item.value;
        return obj;
    }, {});
    // send GET request to server to analyse questions and calculate scores 
    $.getJSON($SCRIPT_ROOT + '/questions/_answers/' + topic + '/' + q_type,
        data,
        function(data) {  //Function carried out when data is received
            // Create outline for table of scores
            html = '<table id="answers" class="table"> <thead> <th> Question</th> <th>Actual Answer</th><th>Your Answer</th><th></th></thead><tbody>'
            //Get returned data
            questions = data.questions
            answers = data.answers
            inputs = data.inputs
            scores = data.scores
            percent = data.percent
            console.log(inputs, answers)
            // For each question/answer which is sent back
            for (var i = 0; i < data.questions.length; i++) {
                // Add row to table with question, correct answer, your answer and a colored
                html += '<tr><td>' + questions[i] + '</td><td>' + '`' + answers[i] + '`' + '</td><td>' + '`' + inputs[i] + '`'
                if (scores[i] === 1) {
                    // Add green coloured square if correct
                    html += '<td bgcolor="#00FF00">'
                } else {
                    // Add red coloured square if wrong
                    html += '<td bgcolor="#FF0000">'
                }
            }
            html += '</tbody></table>'
            // Remove questions form from page, leaving almost empty page
            $('#questions').remove();
            // Add the table to the page
            $(html).appendTo('#main')
            // Typeset maths
            MathJax.Hub.Queue(["Typeset", MathJax.Hub, "answers"]);
        }).fail(function() {
        // An error means that there was invalid input
        alert('Please check your answers')
    })
}
