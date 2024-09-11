import React from 'react'
import { useNavigate } from 'react-router-dom'
import { Auth0Provider } from '@auth0/auth0-react'

const Auth0ProviderWithNavigate = ({ children }) => {
	const navigate = useNavigate()
	const auth0Domain = 'dev-mcfes5f7pf6i3dan.us.auth0.com'
	const auth0ClientId = 'BPGJELgaCdtctLroLuDNcTVGANnBQAM0'

	const onRedirectCallback = appState => {
		navigate(appState?.targetUrl || window.location.pathname)
	}

	return (
		<Auth0Provider
			domain={auth0Domain}
			clientId={auth0ClientId}
			redirectUri={window.location.origin}
			onRedirectCallback={onRedirectCallback}
		>
			{children}
		</Auth0Provider>
	)
}

export default Auth0ProviderWithNavigate
