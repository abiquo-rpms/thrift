#
# Based on the package spec from
# http://github.com/silas/rpms/tree/master/thrift/
#
# Python
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:             thrift
Version:          0.2.0
Release:          1.abiquo
Summary:          A multi-language RPC and serialization framework

Group:            System Environment/Libraries
License:          ASL 2.0
URL:              http://incubator.apache.org/thrift
Source0:          http://www.apache.org/dist/incubator/thrift/%{version}-incubating/%{name}-%{version}-incubating.tar.gz
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:    byacc
BuildRequires:    boost-devel >= 1.33.1
BuildRequires:    flex
BuildRequires:    libevent-devel
BuildRequires:    libtool
BuildRequires:    zlib-devel

%description
Thrift is a software framework for scalable cross-language services
development. It combines a powerful software stack with a code generation
engine to build services that work efficiently and seamlessly between C++,
Java, C#, Python, Ruby, Perl, PHP, Objective C/Cocoa, Smalltalk, Erlang,
Objective Caml, and Haskell.

%package cpp
Summary:          Libraries for %{name}
Group:            Development/Libraries

%description cpp
Libraries bindings for %{name}.

%package cpp-devel
Summary:          Development files for %{name}
Group:            Development/Libraries
Requires:         %{name}-cpp = %{version}-%{release}

%description cpp-devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package python
Summary:          Python bindings for %{name}
Group:            Development/Libraries
BuildRequires:    python-devel

%description python
Python bindings for %{name}.

%prep
%setup -q

# Fix spurious-executable-perm warning
find tutorial/ -type f -exec chmod 0644 {} \;

# Haskell setup script won't run with blank or comment lines
sed -i '/#/d;/^$/d' lib/hs/Setup.lhs

%build
%configure --without-perl --without-erlang --without-java --without-perl --without-ruby --enable-static=no
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

# Install everything not listed below
%{__make} DESTDIR=%{buildroot} install
# Remove "la" files
find %{buildroot} -type f -name "*.la" -exec rm -f {} ';'

# Fix non-standard-executable-perm
%{__chmod} 0755 %{buildroot}%{python_sitearch}/%{name}/protocol/fastbinary.so

%clean
%{__rm} -rf %{buildroot}

%post cpp -p /sbin/ldconfig

%postun cpp -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc CHANGES CONTRIBUTORS LICENSE NEWS NOTICE README doc/ tutorial/
%{_bindir}/thrift

%files cpp
%defattr(-,root,root,-)
%doc LICENSE
%{_libdir}/*.so.*

%files cpp-devel
%defattr(-,root,root,-)
%doc tutorial/README tutorial/cpp tutorial/*.thrift
%{_includedir}/thrift
%{_libdir}/*.so
%{_libdir}/pkgconfig/thrift*

%files python
%defattr(-,root,root,-)
%doc lib/py/README tutorial/py tutorial/*.thrift
%{python_sitearch}/%{name}
%if 0%{?fedora}  > 9
%{python_sitearch}/Thrift-*.egg-info
%endif

%changelog
* Thu Sep 09 2010 Sergio Rubio <srubio@abiquo.com> - 0.2.0-1.abiquo
- Initial Release
