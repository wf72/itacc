import ldap
 
l = ldap.initialize("ldap://192.168.1.5")
try:
    l.protocol_version = ldap.VERSION3
    l.set_option(ldap.OPT_REFERRALS, 0)
 
    bind = l.simple_bind_s("wf@rif-invest.local", "oobe8eSho")
 
    base = "dc=rif-invest, dc=local"
    #criteria = "(&(objectClass=user)(sAMAccountName=username))"
    criteria = "(&(mail=*)(!(userAccountControl:1.2.840.113556.1.4.803:=2))(objectClass=user))"
    attributes = ['sn','givenName', 'mail','telephoneNumber', 'mobile', 'l', 'streetAddress','department','company','displayName','sAMAccountName',]
    result = l.search_s(base, ldap.SCOPE_SUBTREE, criteria, attributes)
    results = [entry for dn, entry in result if isinstance(entry, dict)]
    for contact in results:
        #print contact
        print contact['sAMAccountName'][0]
        #for key in contact.keys():
         #   if key=='sn':
          #      print "FIO: %s" % contact[key][0]
           # print contact[key][0]
finally:
    l.unbind()
 
