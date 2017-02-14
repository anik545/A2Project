$('#submit').on('click', function() {
    submit_answers()
});

function submit_answers() {
    var data = $('#questions').serializeArray().reduce(function(obj, item) {
        obj[item.name] = item.value;
        return obj;
    }, {});
    $.getJSON($SCRIPT_ROOT + '/questions/_answers/' + topic + '/' + q_type,
        data,
        function(data) {
            html = '<table id="answers" class="table"> <thead> <th> Question</th> <th>Actual Answer</th><th>Your Answer</th><th></th></thead><tbody>'
            questions = data.questions
            answers = data.answers
            inputs = data.inputs
            scores = data.scores
            percent = data.percent
            console.log(inputs, answers)
            for (var i = 0; i < data.questions.length; i++) {
                html += '<tr><td>' + questions[i] + '</td><td>' + '`' + answers[i] + '`' + '</td><td>' + '`' + inputs[i] + '`'
                if (scores[i] === 1) {
                    html += '<td bgcolor="#00FF00">'
                } else {
                    html += '<td bgcolor="#FF0000">'
                }
            }
            html += '</tbody></table>'
            $('#questions').remove();
            $(html).appendTo('#main')
            MathJax.Hub.Queue(["Typeset", MathJax.Hub, "answers"]);

        }).fail(function() {
        alert('Please check your answers')
    })
}
