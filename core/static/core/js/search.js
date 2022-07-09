$(document).ready(function(){
    $("#issue-title").on('keyup', function(){
        let ajax_url = $(this).attr("data-ajax_url");
        let value = $(this).val();
        $.ajax({
            url: ajax_url,
            data: {
              'search_val': value
            },
            dataType: 'json',
            success: function (data) {
                let matches = data.results;
                let titles = matches.map(({title}) => title);
                $("#issue-title").autocomplete({
                appendTo: '#autocomplete-cont',
                source: titles,
                minLength: 2
                });
            }
        });
    });
});