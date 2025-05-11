function loadgroups(url, year) {
    var departmentId = document.getElementById('id_department').value;    

    var name = 'group';
    var select_name = 'group';
    var data = { 'department_id': departmentId, 'year': year };
    var idKey = 'id';
    var valueKey = 'number';
    basicAjaxUpdate(url, data, name, select_name, idKey, valueKey);
}


function loadClasses(url) {
    var groupId = document.getElementById('id_group').value;

    $.ajax({
        url: url,
        type: 'POST',
        data: { 'group': groupId },
        headers: {'X-CSRFToken': csrfToken},
        success: function (data) {
            $("#id_classs").html('<option value="" disabled selected="">Select a Class</option>');  
            for (var i = 0; i < data.length; i++) {
                $("#id_classs").append(
                    '<option value="' + data[i].id + '">' + data[i].number + '</option>'
                );
            }
        },
        error: function (xhr, status, error) {
            console.log("Error:", xhr.responseText);
        }
    });
}
