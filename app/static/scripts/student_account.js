// js for sidebar formatting
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
// Initialise imagepicker
$('#graph-select').imagepicker({show_label:true})
$('#links-table').on('click','[type=button]',function(){
  if (confirm('Are you sure')) {
    // Send data of student to be deleted to server
    teacher_id = $(this).attr('id');
    console.log(teacher_id);
    $.post($SCRIPT_ROOT + '/_delete_teacher',{
      teacher_id:teacher_id
    },function(data){
      // Remove teacher from account page
      $('#link-row'+teacher_id).remove()
    }).fail(function(){
      // Show error message if there is a server error
      alert('Error deleting teacher')
    });
  }
});
$('input[type="button"][id*="del-graph"]').on('click',function(){
  if (confirm('Are you sure')) {
    graph_id = $(this).attr('id').replace('del-graph','');
    // Send data of graph to be deleted to server
    $.post($SCRIPT_ROOT + '/_delete_graph',{
      graph_id:graph_id
    },function(data){
      // Remove graph from account page
      $('option[value="'+graph_id+'"]').remove()
      $('#graph-select').imagepicker({show_label:true})
    }).fail(function(){
      // Show error message if there is a server error
      alert('Error Deleting Graph')
    });
  }
});
