
$('#submit').on('click',function(){
    submit_answers()
});

function submit_answers(){
    var data = $('#questions').serializeArray().reduce(function(obj, item) {
            obj[item.name] = item.value;
            return obj;
        }, {});
    $.getJSON($SCRIPT_ROOT + '/questions/_answers/_matrix/'+q_type,
        data, function(data){
    }).fail(function(){
        alert('Please check your answers')
    })
}
