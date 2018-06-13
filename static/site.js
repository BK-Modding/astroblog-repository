$(document).ready(function() {
    M.AutoInit();
    $('.dropdown-trigger').dropdown({
        constrainWidth: false,
        coverTrigger: false
    });
    $('.sidenav').sidenav({
        edge: 'right',
        draggable: true,
        preventScrolling: false
    });
});
