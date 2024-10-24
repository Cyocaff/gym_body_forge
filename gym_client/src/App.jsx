import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Login } from './pages/login.jsx'; // Make sure to capitalize here
import { Navbar } from './components/navbar.jsx'
import { Base } from './pages/base.jsx'
function App() {
    return (
        <BrowserRouter>
		<Navbar/>
            <Routes>
				<Route path="/" element={<Base/>}/>
                <Route path="/login" element={<Login />} /> {/* Use the capitalized component here */}
            </Routes>
        </BrowserRouter>
    );
}

export default App;

