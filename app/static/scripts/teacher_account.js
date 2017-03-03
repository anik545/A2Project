$('#nav').affix({
    offset: {
        top: $('#nav').offset().top
    }
});
$('#nav').affix({
    offset: {
        bottom: ($('footer').outerHeight(true) +
                $('.application').outerHeight(true)) +
                40
    }
});
$('#graph-select').imagepicker({show_label:true})
$('#links-table').on('click','[type=button]',function(){
  if (confirm('Are you sure')) {
    student_id = $(this).attr('id');
    // Send data of student to be deleted to server
    $.post($SCRIPT_ROOT + '/_delete_student',{
      student_id:student_id
    },function(data){
      // Delete all other references to this student on account page
      $('#link-row'+student_id).remove()
      $('#task-row'+student_id).remove()
      $('input[type="checkbox"][value="'+student_id+'"]').parents('tr').remove()
    }).fail(function(){
      // Show error message if there is a server error
      alert('Error deleting Student')
    });
  }
});
$('input[type="button"][id*="del-graph"]').on('click',function(){
  if (confirm('Are you sure')) {
    graph_id = $(this).attr('id').replace('del-graph','');
    // Send data of student to be deleted to server
    $.post($SCRIPT_ROOT + '/_delete_graph',{
      graph_id:graph_id
    },function(data){
      $('option[value="'+graph_id+'"]').remove()
      $('#graph-select').imagepicker({show_label:true})
    }).fail(function(){
      // Show error message if there is a server error
      alert('Error Deleting Graph')
    });
  }
});
