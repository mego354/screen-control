const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

function basicAjaxUpdate(url, data, name, select_name, idKey, valueKey) {
    $.ajax({
        url: url,
        type: 'POST',
        data: data,
        headers: {'X-CSRFToken': csrfToken},
        success: function (response) {
            $(`#id_${name}`).html(`<option value="" disabled selected="">Select a ${select_name}</option>`);  
            for (var i = 0; i < response.length; i++) {
                $(`#id_${name}`).append(
                    '<option value="' + response[i][idKey] + '">' + response[i][valueKey] + '</option>'
                );
            }
        },
        error: function (xhr, status, error) {
            $(`#id_${name}`).html(`<option value="" disabled selected="">Select a ${select_name}</option>`);
            // console.error('status:', status, 'Error:', error);
        }
    });
}
