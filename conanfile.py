# This file is managed by Conan, contents will be overwritten.
# To keep your changes, remove these comment lines, but the plugin won't be able to modify your requirements

from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps
import os
import shutil
from conan.tools.cmake import cmake_layout
from conan.tools.files import copy

class ConanApplication(ConanFile):
    name = "werock_share"
    version = "1.0.0"

    settings = "os", "compiler", "build_type", "arch"

    exports_sources = "include/*", "fbs/*", "sbe/*", "CMakeLists.txt"
    no_copy_source = True

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generate()

    def build(self):
        script_path = os.path.join(self.source_folder, "sbe/schema.xml")
        include_path = os.path.join(self.source_folder, "include")
        shutil.rmtree(include_path, ignore_errors=True)
        jar_path = os.path.join(self.source_folder, "sbe/sbe-all-1.35.6.jar")
        self.run("java -Dsbe.target.language=Cpp -Dsbe.output.dir=%s -jar %s %s" % (include_path, jar_path, script_path))

        source = os.path.join(include_path, 'WeRock_Share_Sbe')
        parent = os.path.dirname(source)
        for f in os.listdir(source):
            shutil.move(os.path.join(source, f), parent)
        os.rmdir(source)

        scheme_files = [os.path.join(self.source_folder, "fbs/Enum.fbs"),
                        os.path.join(self.source_folder, "fbs/Shared.fbs"),
                        os.path.join(self.source_folder, "fbs/Rpc.fbs"),
                        os.path.join(self.source_folder, "fbs/Strategies.fbs")]
        self.run("flatc --cpp -o %s %s" % (include_path, " ".join(scheme_files)))

        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        copy(self, "*.h", self.source_folder, self.package_folder)

    def package_info(self):
        self.cpp_info.bindirs = []
        self.cpp_info.libdirs = []
    def layout(self):
        cmake_layout(self)