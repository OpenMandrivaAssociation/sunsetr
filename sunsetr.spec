%global debug_package %{nil}

Name:		sunsetr
Version:	0.7.0
Release:	1
Source0:	https://github.com/psi4j/sunsetr/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:	%{name}-%{version}-vendor.tar.gz
Summary:	Autmoatic blue light filter for hyprland, Niri, and everything Wayland
URL:		https://github.com/psi4j/sunsetr
License:	MIT
Group:		Window Manager/Utility

BuildRequires:	cargo

%description
%summary.

%prep
%autosetup -p1
tar -zxf %{SOURCE1}
mkdir -p .cargo
cat >> .cargo/config.toml << EOF
[source.crates-io]
replace-with = "vendored-sources"

[source.vendored-sources]
directory = "vendor"
EOF

%build
cargo build --frozen --release

%install
install -dm0755 %{buildroot}%{_bindir}
install -dm0755 %{buildroot}%{_userunitdir}
install -Dm0755 target/release/%{name} %{buildroot}%{_bindir}
install -Dm0644 %{name}.service %{buildroot}%{_userunitdir}/

%preun
%systemd_user_preun %{name}.service

%post
%systemd_user_post %{name}.service
echo "Sunsetr is not compatible with hyprsunset service, you can disable it with:"
echo "    systemctl --user disable hyprsunset.service"

%files
%doc README.md
%license LICENSE
%{_bindir}/%{name}
%{_userunitdir}/%{name}.service
