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
# OSISoft Internship - Week 5

Here is a quick summary of my fifth week.

## Where I was

I found where was the delay located but I still had to build the library myself from sources so I can then modify it.

## What I did

### Building the library

I first installed an entire VM with every components needed to build the library (VS2010, SDK7.1, gow, perl, etc.). I finished building the **debug library** so I can locate what is taking so long in `gss_init_sec_context()`.

Found what part of the function is too long :
`gss_init_sec_context` -> `gssint_import_internal_name` -> `krb5_gss_import_name` -> `krb5_sname_to_principal` -> `canon_hostname` - > `getnameinfo`

>The getnameinfo function is the ANSI version of a function that provides protocol-independent name resolution. The getnameinfo function is used to **translate** the contents of a **socket address** structure to a node name and/or a **service name**.

One way to highlight this issue is making the canonicalization before calling gss_init_sec_context so the delay is just in this exaction of the name :
``` c++

majStat = gss_import_name(&minStat, &serviceNameBuffer,GSS_C_NT_HOSTBASED_SERVICE , &gssServiceName);

gss_name_t servName; //The next line is very long (15sec):
gss_canonicalize_name(&minStat, gssServiceName, &gss_krb5_mech_oid_desc, &servName);

// Now this one is really quick :
gss_init_sec_context(&minStat, GSS_C_NO_CREDENTIAL, &ctx, servName, &gss_krb5_mech_oid_desc, GSS_C_DELEG_FLAG,GSS_C_INDEFINITE, GSS_C_NO_CHANNEL_BINDINGS, GSS_C_NO_BUFFER, nullptr, &outputToken, nullptr, nullptr);
```

So the delay is due to the **conversion** between a name using `HOSTBASED_SERVICE` mechanism to a name using `KRB5_PRINCIPAL_NAME` mechanism.

> `HOSTBASED_SERVICE` looks like :&nbsp;&nbsp;&nbsp;&nbsp; service@host.full.domain.name <br>
> `KRB5_PRINCIPAL_NAME` looks like :&nbsp; service/host@REALM

I figured out that `gssint_import_internal_name` is only called if `target_name` and `mech_type` don't match so we have to **convert the name type** witch the function takes in parameter before getting in the function.

So I tried to use the `KRB5_PRINCIPAL_NAME` in the first import_name witch is called before gss_init_sec_context so we don't have to convert it. It turns out that we don't have this delay anymore if we import the internal name using `KRB5_PRINCIPAL_NAME`. It could then be a solution to the bug in the main project !

> _Note 1_ : You have to import the file <gssapi/gssapi-krb5.h> in order to use `KRB5_PRINCIPAL_NAME` <br>
> _Note 2_ : We avoid the long part of the function so we still can use the original library

### Building the ODBC client with modifications

The next step was to build the project with my modifications. That is what we did and I just used the dll generated in my previous installation and we couldn't see the delay anymore.

The first mission of my internship is then accomplished.

### Finding alternative libraries

The next part is finding another solution to make the same double hop connection. Indeed there are two big issues with the solutions used :
* The company doesn't want to use **openSSL** anymore
* We want a solution witch doesn't require admin permissions on the **Domain Controller**
* We still want to use **kerberos** authentication

> Quick sumary of solutions we have
>
> -                 | winHTTP | GSS-API | SSPI
> -------------------|---------|---------|------
> Need domain admin | Yes     | No      | ?    
> Use OpeSSL        | No      | Yes     | No   
> Double Hop        | NO      | yes     | ?    
>
>Double hop senario :
>* Client uses credentials to get his **TGT** from the KDC
>* Client gets a **ticket for connecting to server 1** using the TGT
>* Client connects to server 1
>* Server 1 uses the client's TGT to ask for a **ticket for connecting to server 2**
>* Servers 1 connects to server 2 using Client's credentials

## What I have to do


* See if I can tweak winhttp to turn on **deleg_req_flag** and don't use the DC
* What is Heimdal ?
* Can we use krb5_functions ?
* Find a solution witch fits every needs.
