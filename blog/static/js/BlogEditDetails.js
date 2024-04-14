class LinkTitleBlockDefinition extends window.wagtailStreamField.blocks
    .StructBlockDefinition {
    render(placeholder, prefix, initialState, initialError) {
        const block = super.render(
            placeholder,
            prefix,
            initialState,
            initialError,
        );

        let allOptions = [];
        const titleField = document.getElementById(prefix + '-title');
        const urlField = document.getElementById(prefix + '-url');
        $.ajax({
            url: '/get_links_options/',
            type: 'GET',
            success: function(data) {
                allOptions = data.map(function(item) {
                    return {
                        title: item.title,
                        url: item.url
                    }
                })
            }
        });

        const fieldChanggeHandler = () => {
            let title = titleField.value.trim();
            for (let option of allOptions) {
                if (option.title.toLowerCase() === title.toLowerCase()) {
                    urlField.value = option.url;
                    break;
                }
            }
        }
        titleField.addEventListener('input', fieldChanggeHandler);

        return block;
    }
}
window.telepath.register('blog.models.LinkTitleBlock', LinkTitleBlockDefinition);
