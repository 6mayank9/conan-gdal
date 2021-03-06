
import os
from conans import ConanFile, AutoToolsBuildEnvironment, tools
from conans.tools import download, unzip

class GdalConan(ConanFile):
    """ Conan package for GDAL """

    name = "GDAL"
    version = "2.1.3"
    description = "GDAL - Geospatial Data Abstraction Library"
    url = "http://www.gdal.org/"
    license = "LGPL"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = {"shared": True}
    requires = "zlib/1.2.11@conan/stable"
    exports = ["LICENSE.md", "FindGDAL.cmake"]

    _folder = "gdal-%s" % version


    def requirements(self):
        if not self.options.shared:
            self.requires("sqlite3/3.27.1@bincrafters/stable", private=False, override=False)


    def source(self):
        archive_name = "gdal-%s.tar.gz" % self.version
        src_url = "http://download.osgeo.org/gdal/%s/%s" % (self.version, archive_name)

        download(src_url, archive_name)
        unzip(archive_name)
        os.unlink(archive_name)
        if self.settings.os != "Windows":
            self.run("chmod +x ./%s/configure" % self._folder)


    def build(self):
        config_args = ["--with-geos=yes"]
        if self.options.shared:
            config_args += ["--disable-static", "--enable-shared"]
        else:
            config_args += [
                "--without-ld-shared", "--disable-shared", "--enable-static",
            ]

        autotools = AutoToolsBuildEnvironment(self)
        with tools.chdir(self._folder):
            autotools.configure(args=config_args)
            autotools.make()
            autotools.install()

        self.run("cp %s/FindGDAL.cmake %s/" % (self.source_folder, self.package_folder))


    def package_info(self):
        self.cpp_info.includedirs = ["include"]
        self.cpp_info.libs = ["gdal"]
