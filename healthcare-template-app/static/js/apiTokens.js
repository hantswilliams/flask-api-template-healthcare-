function copyToken() {
    var copyText = document.getElementById("apiToken");
    copyText.select();
    copyText.setSelectionRange(0, 99999); /* For mobile devices */
    navigator.clipboard.writeText(copyText.value);
    alert("Copied the token: " + copyText.value);
}