(function () {
    'use strict';
  
    window.addEventListener('load', function () {
      // Form validation
      var forms = document.querySelectorAll('.needs-validation');
      Array.prototype.forEach.call(forms, function (form) {
        form.addEventListener('submit', function (event) {
          if (!form.checkValidity()) {
            event.preventDefault();
            event.stopPropagation();
          }
          form.classList.add('was-validated');
        }, false);
      });
  
      // Handle signup form submission
      $('#signupForm').submit(function (event) {
        event.preventDefault();
  
        // Collect user data
        var username = $('#username').val();
        var email = $('#email').val();
        var phone = $('#phone').val();
        var age = $('#age').val();
  
        // Send user data to server for OTP generation (replace with your logic)
        $.ajax({
          url: '/generate_otp', // Replace with your server-side endpoint
          method: 'POST',
          data: {
            username: username,
            email: email,
            phone: phone,
            age: age
          },
          success: function (response) {
            // Handle successful OTP generation
            console.log('OTP generated successfully:', response);
            $('#signupForm').hide();
            $('#otpForm').show();
          },
          error: function (error) {
            // Handle errors during OTP generation
            console.error('Error generating OTP:', error);
            // Display error message to the user
          }
        });
      });
  
      // Handle OTP form submission
      $('#otpForm').submit(function (event) {
        event.preventDefault();
  
        // Collect OTP
        var otp = $('#otp').val();
  
        // Send OTP to server for verification (replace with your logic)
        $.ajax({
          url: '/verify_otp', // Replace with your server-side endpoint
          method: 'POST',
          data: {
            otp: otp
          },
          success: function (response) {
            // Handle successful OTP verification
            console.log('OTP verified successfully:', response);
            // Complete signup process (e.g., redirect to user profile)
          },
          error: function (error) {
            // Handle errors during OTP verification
            console.error('Error verifying OTP:', error);
            // Display error message to the user
          }
        });
      });
    });
  })();
  