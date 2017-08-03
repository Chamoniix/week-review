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
# OSISoft Internship - Week 3

Here is a quick summary of my third week.

## Where I was

At the end of the previous week, I had learned a lot about the Pi System and how it works *(specially the double-hop senario using kerberos)* and what is composing it. I had my small "local lab"
with the simplest Pi System. But I still didn't know anything about the real development that I was about to begin.

## What I did

That's why I had a lot of things to do this week :

1. The first was to **install my environment** in the development team *(transfer of VM and installing IDE)*

2. Then I tried to understand excatcly what will I have to do during this project. It turns out finally that I will have to develop a totally independent application using the same technologies as
the ODBC client and the DAS server : **windows sockets** for the connection, **Kerberos**, **GSS-API** and maybe **SSPI** for authentication.

3. From here I tried to compile a lot of sample projects. The first difficulty I had was **finding the good libraries and importing those in my projects**. I finally succeed to be able to use all the gss functions and variables. Nevertheless, every projects samples that I could found were either for windows platform or out-of-date *(functions using OLD C instead of ANSI C declaration witch aren't compatible with Visual 2017 and other)*.

4. I then used the samples to understand how the sequence of execution was executed by the different samples, witch were, in my opinion, too complicated for the basic connection,to then **create my very own project**. I specially used this [course](https://docs.oracle.com/cd/E19683-01/816-1331/) witch contains a course about GSS-API, ans sample project and a complete walk-through of this example; this [git](https://github.com/BeyondTrust/pbis-open) in witch I found some windows samples and [Microsoft website](https://msdn.microsoft.com) for diplaying errors. For now I did :
 * The client importing name of the server
 * The client connection
 * The client asking for security context
 * The server connection via windows sockets
 * The server acquire is own internal name

## What I have to do

At the end of the week I was stuck on the server side on the function **gss_acquire_credentials**. So I will try next week to resolve the credentials acquiring ans the to **accept the security context**.
