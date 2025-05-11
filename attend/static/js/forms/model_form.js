document.querySelectorAll('.fotd').forEach(function (form) {
    form.addEventListener('submit', function () {
      document.querySelectorAll(".DV").forEach(dv => {
        dv.value = WURFL.complete_device_name; 
      });
    });
  });
