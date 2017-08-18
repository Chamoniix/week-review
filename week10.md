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
.codeTitle {
  font-style: italic;
  line-height: 0%;
  font-size: 80%;
}
</style>
# OSISoft Internship - Week 10

Here is a quick summary of my tenth week.

## Where I was

This week I really have to finish my presentation as I will present it next week, and I may will make a rehearse with those who want to before the real presentation. Moreover, I will have to explain why we are using SSL with GSS API which is still not clear for me so I will have to clarify all of this.

## What I did

First of all I spend a big part of the beginning of the week to finish the presentation and prepare a demo which would correspond to the presentation. Important for the demo :
* fradev-t3-DAS4
* fradev-t2-AF28  -  *Trusted*
* fradev-t2-AF27  -  *Not Trusted*

Difficulties to have to same behaviour on OSI domain, whereas Ramata has the exact same behaviour as I have on fratest domain when using the same dll. To find where the problem can be I tried to use `process explorer`

It was realy complecated to have the connection working, I spent 3 days of the week with Ramata's help trying to have it working because when I was trying to use my OSI domain computeur the ticket couldn't be acquired from the application and I had to execute a `kinit` but then I didn't have this delay anymore has it comes from the ticket acquiring. Eventually I had it working on Natalia's computer on which I installed everything from scratch and then it was behaving the was it is supposed to. So I will use a remote session on her computer for the presentation day.

### OpenSSL in our project

I could still not understand why do we need openSSL in our project, whereas the only goal of Kerberos is authentication with a secured connection already encrypted. Infact openSSL insn't used for authentication in our project, it is used for every following communication which happen after the authentication and which cannot be in clear text. Then openSSL is the only way no enable HTTPS with GSOAP so if we wan't to keep GSoap we will have to keep openSSL:

> To utilize HTTPS/SSL, you need to install the OpenSSL library on your platform or GNUTLS for a light-weight SSL/TLS library. After installation, compile all the sources of your application with option -DWITH_OPENSSL

WinHTTP in it self is taking care of authentication but also of the HTTPS communication which happens next. That's why it is not using openSSL.

||
|---------------|
| Application   |
| Presentation  |
| session       |
| **Transport** |
| Network       |
| Data Link     |
| Physical      |

Useful tool `sysdm.cpl`

## What I have to do
