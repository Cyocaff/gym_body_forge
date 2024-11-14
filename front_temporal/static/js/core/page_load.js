let token = localStorage.getItem('accessToken');
let user_data
let page_data
const publicPages = ['/login','/registrarse','/preguntas','/nosotros']
function logout(){
	localStorage.removeItem('accessToken')
}

function decodeJWT(token) {
    // Split the token into header, payload, and signature
    const [headerB64, payloadB64, signature] = token.split('.');
    // Decode the payload
    function base64UrlDecode(str) {
        // Add padding if needed
        str = str.replace(/-/g, '+').replace(/_/g, '/');
        while (str.length % 4) {
            str += '=';
        }
        // Decode base64
        return atob(str);
    }
    const payload = JSON.parse(base64UrlDecode(payloadB64));   
    return payload;
}
function loadData(path) {
	return $.ajax({
		url: "http://localhost:8000/api/" + path + "/",
		method: 'GET',
		headers: {
        	'Authorization': 'Bearer ' + token
        }
	}).then(function(response) {
		page_data = response; 
		return page_data;
	}).catch(function(error) {
		console.error('Failed to load page data:', error);
		return null;
	})};

if (token){
	user_data = decodeJWT(token);
}

async function loadPage(current_path_name, goback) {
    console.log(current_path_name)
	if (!token && !publicPages.includes(current_path_name)){
		window.location.href = '/login';
	}
	else{

		console.log('logged in')
		if (!publicPages.includes(window.location.pathname)){
		$("#session-manager").html('<a href="" onclick="logout()"><h3>Cerrar sesion</h3></a>');
			await loadData(current_path_name.split('/').pop());	
		}else{
			if (!token){
				$("#session-manager").html('<a href="/registrarse"><h3>Registrarse</h3></a>');
			}else{
				$("#session-manager").html('<a href="" onclick="logout()"><h3>Cerrar sesion</h3></a>');
			}
		}
		
		$.ajax({
        url: current_path_name,
        type: 'GET',
        success: function(response) {
            // Update the content of a specific element with the new HTML
            $('#page_content_body').html(response);
            // Adds the URL to the window history to allow posterior navigation 
            if (!goback){
                window.history.pushState(null, null, current_path_name);
            }
        },
        error: function(xhr, status, error) {
            console.log('AJAX error: ', status, error);
        }
	    });
	}
}

// Adds an event listener for whenever the user uses the navigation
// option of the history of the window, by doing this the parameter
// 'true' is sent to the function to prevent the updating of the history
// this because while navigating the history must not be updated to
// prevent errors or stuff like that.
window.addEventListener('popstate', function(event) {
    loadPage(window.location.pathname,true)
});

window.addEventListener('click', (event) => {
    // Check if the clicked element is an <a> tag with the 'page-navigator' class,
    // this because if the element clicked is a child element of the navigator tag
    //  our event target will not properly work, this makes sure to target the <a>
    // navigator.
    if (event.target.closest('a')?.classList.contains('page-navigator')) {
        event.preventDefault();  // Prevent the default behavior of the anchor tag
        const href = event.target.closest('a').href;  // Get the href from the closest <a> tag
        loadPage(href);  // Call loadPage with the href value
    }
});

