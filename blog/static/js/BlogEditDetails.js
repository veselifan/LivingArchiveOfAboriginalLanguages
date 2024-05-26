class LinkTitleBlockDefinition extends window.wagtailStreamField.blocks
    .StructBlockDefinition {
    render(placeholder, prefix, initialState, initialError) {
        const block = super.render(
            placeholder,
            prefix,
            initialState,
            initialError,
        );

        const body = document.getElementById('wagtail')
        const inputTitleField = document.getElementById(prefix + '-title');
        inputTitleField.setAttribute('type', 'search')
        inputTitleField.setAttribute('autocomplete', 'off')
        const dataList = document.createElement('datalist');
        dataList.id = 'title-list'

        $.ajax({
            url: '/get_links_options/',
            type: 'GET',
            success: function (data) {
                for (let i = 0; i < data.length; i++) {
                    const option = document.createElement('option');
                    option.value = data[i];
                    dataList.appendChild(option);
                }
                body.appendChild(dataList);
                inputTitleField.setAttribute('list', 'title-list')
            }
        });

        return block;
    }
}

window.telepath.register('blog.models.LinkTitleBlock', LinkTitleBlockDefinition);
