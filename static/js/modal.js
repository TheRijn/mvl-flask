$('#detailModal').on('show.bs.modal', function (event) {
    let card = $(event.relatedTarget); // Button that triggered the modal
    let post_id = card.data('post_id');

    $.post(`/api/post/${post_id}`, data => {

        let post = data.post;
        console.log(post);

        $('#details-title').text(post.title);
        $('#details-intro').html(post.intro);
        $('#details-description').html(post.description);

        // $('#details-images').text('');
        // post.images.forEach(image => {
        //     $('#details-images').append(`<img src=${image}>`)
        // });

    });
});