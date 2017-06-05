$(function() {

        $('#btnSubmit').click(function() {
        console.log("This is working so far");

            $.ajax({
                url: '/new_animal_profile',
                data: $('form').serialize(),
                type: 'POST',
                success: function(response) {
                    console.log(response);
                },
                error: function(error) {
                    console.log(error);
                }
            });
    });
});
