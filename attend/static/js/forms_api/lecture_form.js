function loadDepartments(url) {
    var collegeId = document.getElementById('id_college').value;    
    var name = 'department';
    var select_name = 'department';
    var data = { 'college': collegeId };
    var idKey = 'id';
    var valueKey = 'name'; 
    basicAjaxUpdate(url, data, name, select_name, idKey, valueKey);
}
 
function loadCourses(){
    var departmentId = document.getElementById('id_department').value;    
    var yearId = document.getElementById('id_year').value;    
    if (departmentId && yearId){
        var name = 'DepCourse';
        var select_name = 'course';
        var data = { 'department': departmentId, 'year': yearId };
        var idKey = 'id';
        var valueKey = 'course__name';
        basicAjaxUpdate(load_courses, data, name, select_name, idKey, valueKey);

        var name = 'group';
        var select_name = 'group';
        var data = { 'department_id': departmentId, 'year': yearId };
        var idKey = 'id';
        var valueKey = 'number';
        basicAjaxUpdate(load_groups, data, name, select_name, idKey, valueKey);
    }
}

function loadDoctors(url) {
    var CourseId = document.getElementById('id_DepCourse').value;    
    var is_doctor = document.getElementById('id_DepCourse').dataset.doctor === 'true'? true : false;
    var name = 'doctor';
    var select_name = 'doctor';
    var data = { 'course': CourseId , 'doctor':is_doctor};
    var idKey = 'id';
    var valueKey = 'name';
    basicAjaxUpdate(url, data, name, select_name, idKey, valueKey);
}

