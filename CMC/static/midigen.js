$(function(){
    // add listener on all the buttons (on CLICK)
    var buttons = $(".midigen");
    buttons.each(function(index,element){
        $(this).on('click', function(event) {
            a_tag = $(this);
            // If button has been clicked already, href!="", and default action
            // should be executed
            if (a_tag.attr("href")=="" ){
                event.preventDefault();
                console.log("Trying to generate MIDI file");
                // TODO: make the url below 'smart'
                url = "generate_midi/" + String($(this).data("piece"));
                // ask server to generate midi and return url from which
                // it could be downloaded
                $.ajax({
                    url: url,
                    type: "GET",
                    dataType: "json"
                }).done(function(result) {
                    console.log("Server responded:");
                    a_tag.attr("href", result['url']);
                    console.log(result['type']);
                    if (result['type'] == "file"){
                        console.log('Received File');
                        a_tag.attr("download", "");
                    } else if (result['type'] == 'redirect'){
                        // redirect AnonymousUser to login page
                        console.log("Redirecting");
                        a_tag.removeAttr("download");
                    } else {
                        console.log("Failed");
                    };
                    // trigger event again (the href attr has been updated)
                    a_tag.find("button").click();
                }).fail(function(xhr,status,err) {
                    console.log("Failed to generate MIDI file");
                });
            };
        });
    });
});


