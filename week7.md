<style>
body {
  font-size: 14px !important;
  font-family: Inconsolata, Monaco, Consolas, 'Courier New', Courier !important;
  text-align: justify !important;
  text-justify: inter-word !important;
  line-height: 1.45;
  color: #3f3f3f;
}
h1 {
  font-size: 2.6em !important;
  font-family: inherit !important;
  font-weight: 300 !important;
  line-height: 1.1 !important;
  color: inherit !important;
  outline: none !important;
  text-decoration : none !important;
}
h2 {
  font-weight: 300 !important;
  line-height: 1.1 !important;
  color: inherit !important;
  font-size: 2.15em !important;
}
h3 {
  font-weight: 300 !important;
  line-height: 1.1 !important;
  color: inherit !important;
  font-size: 1.8em !important;
}
img {
  display: block;
  margin-left: auto;
  margin-right: auto;
}
</style>
# OSISoft Internship - Week 7

Here is a quick summary of my seventh week.


## Where I was

I still did not found a way to use winHTTP and allowed delegation without trusting the Data Access Server.

## What I did ?

My priority this week was to understand winHTTP, how does it basically work, and then how it is used in the ODBC client. To accomplish this task, I did several things.

### Understanding winHTTP an authentication
First I red the entire [Microsoft article](https://msdn.microsoft.com/en-us/library/windows/desktop/aa382925) about winHTTP which is really complete. It allowed me to learn a lot about the protocol. I also **created my own sample** of connection using Microsoft samples.

This scheme is a really good overview of the winHTTP sessions :
![winhttp](img/winHTTP.png)

In this article they explain a lot about how winHTTP opens a connection and which different options do we have to authenticate a user. So I figured out that, to **be sure to use Kerberos**, we should set the option `WINHTTP_AUTOLOGON_SECURITY_LEVEL_LOW` and use `WINHTTP_AUTH_SCHEME_NEGOTIATE` in the function setCredentials(). With this done the authentication we be done with Kerberos for recent windows versions and NTML if it is older. So I changed it in the ODBC client.

>WINHTTP_AUTOLOGON_SECURITY_LEVEL_LOW using the WinHttpSetOption API. The
"Low" policy setting means that the credentials should always be delegated
(if possible).

So I changed this part of the GSoapWinHTTP plugin from BASIC to NEGOCIATE:
```C++
if (!WinHttpSetCredentials(hHttpRequest, WINHTTP_AUTH_TARGET_SERVER, WINHTTP_AUTH_SCHEME_BASIC, wcuser, wcpsw, nullptr))
```

### How to use Fiddler
I then wanted to verify that the ODBC client is using the kerberos ticket and not the SSPI or NTML connection from windows so it would explain that the delegation is working with GSSAPI and not winHTTP. For this I tried to use **Fiddler** to see the HTTP trafic on the computer. To use it I had to change two things :
* First in the code I added those two lines before the connection to use the Fiddler proxy that will then be forwarded to the Data Access Server:
```C++
// use fiddler
   spThreadContext->proxy.proxy_host = "localhost";
   spThreadContext->proxy.proxy_port = 8888;
```
* But I still couldn't see any trafic from the ODBC client. I then had to execute this bash command : `netsh winhttp set proxy localhost:8888`. Then I could verify every HTTP frame which also helped me to understand the application functionment.

### Test environment for delegation

Then I wanted to find a quick way to check for every changes that I made if the connection was still working with the trusted configuration and if the untrusted was still blocked. But domain changes take quite long to be considerate, so I had to **create another Data Access Server** which is trusted and one which isn't.

I also tried to use **DelegConfig** which is a delegation testing tool from Microsoft but it was quite complicated to use so I didn't spend much time on it but if I need I know I could try to use it.

### How to enable winHTTP delegation ?

I tried a lot a things to enable this delegation flag. First I read something in the GSoapWinHTTP documentation :
> For extra control, you may also register this plugin using the
soap_register_plugin_arg() function, and supply as the argument flags which
you want to be passed to HttpOpenRequest.

So I through I have to configure it but I didn't know how. Then I found every single [flag](https://msdn.microsoft.com/en-us/library/windows/desktop/aa384066) that you can use with winHTTP. So I tried a lot of them but I never had the delegation allowed. Specially the `WINHTTP_ENABLE_SSL_REVERT_IMPERSONATION` is creating an error but it looks like it could be something I want to enable.

I also read a really interesting [article](http://microsoft.public.winhttp.narkive.com/X3Ao0QcV/winhttp-credentials-delegation) written by someone trying to use winhttp delegation but not with gsoap and kerberos.

With every flags that I tried I couldn't forward the credentials, so maybe I have to change the setCredentials function ; but there is one thing which is surprising me and make me wonder if delegation with winhttp is possible from Microsoft Library :
> The credentials set by WinHttpSetCredentials are only used for a single request; WinHTTP does not cache these credentials for use in subsequent requests

## What I have to do

I found a lot more information about how to configure winHTTP and I could for the first time really change the ODBC client and see the changes. But still I cannot really see where is the error coming from.

I think for next week I will try to debug the Data Access Server to see **exactly where is the connection blocked** : if the connection with the DAS is OK without the trust and which credentials the DAS is trying to use to connect to the AF.

> Look for more information about **httpg**

> For presentation : don't forget to talk about `ImpersonateSecurityContext` from gssapi


Projet test gsoap [sample](http://r0d.developpez.com/articles/tuto-gsoap-fr/)
