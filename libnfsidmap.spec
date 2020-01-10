%define _root_libdir    /%{_lib}

Summary: NFSv4 User and Group ID Mapping Library
Name: libnfsidmap
Version: 0.25
Release: 17%{?dist}
Provides: libnfsidmap
Obsoletes: nfs-utils-lib
URL: http://www.citi.umich.edu/projects/nfsv4/linux/
License: BSD

Source0: http://www.citi.umich.edu/projects/nfsv4/linux/libnfsidmap/%{name}-%{version}.tar.gz

Patch001: libnfsidmap-0.26-rc3.patch
Patch002: libnfsidmap-0.25-zero-ids.patch
Patch003: libnfsidmap-0.25-nobody.patch
Patch004: libnfsidmap-0.25-strrchr.patch
Patch005: libnfsidmap-0.25-warnings.patch
#
# RHEL7.2
#
Patch006: libnfsidmap-0.25-nullnames.patch
#
# RHEL7.3
#
Patch007: libnfsidmap-0.2-stripnewlines.patch
Patch008: libnfsidmap-0.2-negativerets.patch
Patch009: libnfsidmap-0.2-memleak.patch
#
# RHEL7.4
#
Patch010: libnfsidmap-0.25-multidomain.patch
Patch011: libnfsidmap-0.25-dns-resolved.patch
Patch012: libnfsidmap-0.25-nssgssprinc.patch

Group: System Environment/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: pkgconfig, openldap-devel
BuildRequires: automake, libtool
Requires(postun): /sbin/ldconfig
Requires(pre): /sbin/ldconfig
Requires: openldap

%description
Library that handles mapping between names and ids for NFSv4.

%package devel
Summary: Development files for the libnfsidmap library
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
This package includes header files and libraries necessary for
developing programs which use the libnfsidmap library.

%prep
%setup -q 

%patch001 -p1 

#
# RHEL7.1
#
# 1093093 - chown does not respect NFSv4 no_root_squash
%patch002 -p1 
# 1129790 - libnfsidmap: respect Nobody-User/Nobody-Group
%patch003 -p1 
# 1114053 - RFE: Make rpcidmap and NFS accept full qualified usernames as a user.
%patch004 -p1 
# 1152658 - A large number of warning occur when the source is compiled
%patch005 -p1 
# 1214882 - libnfsidmap: crash due to not checking argument
%patch006 -p1 
# 1261124 - libnfsidmap: strip newlines out of IDMAP_LOG messages
%patch007 -p1 
# 1271449 - "Covscan test" failures in errata RHBA-2015:20444-05....
%patch008 -p1 
%patch009 -p1 
# 1378557 - NFSv4 id mapping issues in multi-domain environments 
%patch010 -p1 
# 980925 - rpc.idmapd should support getting the NFSv4 ID Domains from DNS
%patch011 -p1 
# 1420352 - Cannot create file in it's directory using kerberos....
%patch012 -p1 

rm -f configure.in

%build
./autogen.sh
%configure --disable-static  --with-pluginpath=%{_root_libdir}/%name
make %{?_smp_mflags} all

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} \
    libdir=%{_root_libdir} pkgconfigdir=%{_libdir}/pkgconfig

mkdir -p %{buildroot}%{_sysconfdir}
mkdir -p %{buildroot}%{_mandir}/man5

install -m 644 idmapd.conf %{buildroot}%{_sysconfdir}/idmapd.conf

# Delete unneeded libtool libs
rm -rf %{buildroot}%{_root_libdir}/*.{a,la}
rm -rf %{buildroot}%{_root_libdir}/%{name}/*.{a,la}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog NEWS README COPYING
%config(noreplace) %{_sysconfdir}/idmapd.conf
%{_root_libdir}/*.so.*
%{_root_libdir}/%{name}/*.so
%{_mandir}/*/*

%files devel
%defattr(0644,root,root,755)
%{_libdir}/pkgconfig/libnfsidmap.pc
%{_includedir}/nfsidmap.h
%{_root_libdir}/*.so

%changelog
* Fri Feb 17 2017 Steve Dickson <steved@redhat.com> 0.25-17
- Fixed stripping realm problem in nss_gss_princ routines (bz 1420352)

* Tue Jan 10 2017 Steve Dickson <steved@redhat.com> 0.25-16
- Add options to aid id mapping in multi domain environments (bz 1378557)
- Query DNS for the the NFSv4 domain (bz 980925)

* Wed Aug 17 2016 Steve Dickson <steved@redhat.com> 0.25-15
- nss_getpwnam: correctly check for negative values (bz 1271449)
- Fixed a memory leak in nss_name_to_gid() (bz 1271449)

* Thu Apr  7 2016 Steve Dickson <steved@redhat.com> 0.25-13
- Strip newlines out of IDMAP_LOG messages (bz 1261124)
- Fixed some NEGATIVE_RETURNS that a Covscan scan found (bz 1271449)

* Mon May  4 2015 Steve Dickson <steved@redhat.com> 0.25-12
- Handle NULL names better (bz 1214882)

* Tue Oct 21 2014 Steve Dickson <steved@redhat.com> 0.25-11
- Accept full qualified usernames a a user (bz 1114053)
- Removed a number of warnings (bz 1152658)

* Wed Sep 17 2014 Steve Dickson <steved@redhat.com> 0.25-10
- id_as_chars() fails zero value ids (bz 1093093)
- respect Nobody-User/Nobody-Group (bz 1129790)

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 0.25-9
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.25-8
- Mass rebuild 2013-12-27

* Mon Aug 19 2013 Ville Skyttä <ville.skytta@iki.fi> - 0.25-7
- Updated to latest rc release: libnfsidmap-0-26-rc3

* Fri Jul 26 2013 Ville Skyttä <ville.skytta@iki.fi> - 0.25-6
- Drop unnecessary doc dir references from specfile.
- Fix bogus dates in %%changelog.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.25-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.25-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 19 2012 Steve Dickson <steved@redhat.com>  0.20-3
- Updated to latest rc release: libnfsidmap-0-26-rc1

* Mon Mar 19 2012 Steve Dickson <steved@redhat.com>  0.20-2
- Fixed Local-Realms debugging (bz 804152)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.25-1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec  6 2011 Steve Dickson <steved@redhat.com>  0.20-0
- Updated to latest release: libnfsidmap-0.25

* Mon Nov 14 2011 Steve Dickson <steved@redhat.com>  0.24-7
- Updated to latest rc release: libnfsidmap-0-25-rc3 (bz 753930)

* Mon Mar  7 2011 Steve Dickson <steved@redhat.com>  0.24-6
- Updated to latest rc release: libnfsidmap-0-25-rc2

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.24-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 14 2011 Steve Dickson <steved@redhat.com>  0.24-4
- Updated to latest rc release: libnfsidmap-0-25-rc1

* Wed Dec 22 2010 Steve Dickson <steved@redhat.com>  0.24-3
- Used the newly added --with-pluginpath config flag to 
  redefine where the plugins live (bz 664641).

* Fri Dec 10 2010 Steve Dickson <steved@redhat.com>  0.24-2
- Removed the versions from the Provides: and Obsoletes: lines

* Wed Dec  8 2010 Steve Dickson <steved@redhat.com>  0.24-1
- Updated to latest upstream release: 0.24
- Obsoleted nfs-utils-lib

* Tue Dec  7 2010 Steve Dickson <steved@redhat.com>  0.23-3
- Maded corrections in spec per review comments.

* Fri Dec  3 2010 Steve Dickson <steved@redhat.com>  0.23-2
- Initial commit
