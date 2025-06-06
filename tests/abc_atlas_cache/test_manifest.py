import json
from pathlib import Path
import pytest
import unittest
from abc_atlas_access.abc_atlas_cache.manifest import Manifest, DataTypeNotInDirectory


class TestManifest(unittest.TestCase):

    def setUp(self):
        self.cache_dir = "/my/cache/dir/"
        self.manifest_path = (
            Path(__file__).parent / "resources" / "manifest.json"
        )  # noqa: E501

    def test_init(self):
        """
        Test that the Manifest class can be instantiated
        """
        with open(self.manifest_path, "r") as jfile:
            manifest = Manifest(cache_dir=self.cache_dir, json_input=jfile)

        with open(self.manifest_path, "r") as jfile:
            test_data = json.load(jfile)

        assert manifest.data == test_data
        assert manifest.version == test_data["version"]
        assert manifest.resource_uri == test_data["resource_uri"]
        assert manifest.list_directories == [
            "ASAP-PMDBS-10X",
            "ASAP-PMDBS-taxonomy",
            "Allen-CCF-2020",
            "HMBA-10xMultiome-BG",
            "HMBA-10xMultiome-BG-Aligned",
            "HMBA-BG-taxonomy-CCN20250428",
            "MERFISH-C57BL6J-638850",
            "MERFISH-C57BL6J-638850-CCF",
            "MERFISH-C57BL6J-638850-imputed",
            "MERFISH-C57BL6J-638850-sections",
            "SEAAD",
            "SEAAD-taxonomy",
            "WHB-10Xv3",
            "WHB-taxonomy",
            "WMB-10X",
            "WMB-10XMulti",
            "WMB-10Xv2",
            "WMB-10Xv3",
            "WMB-neighborhoods",
            "WMB-taxonomy",
            "Zeng-Aging-Mouse-10Xv3",
            "Zeng-Aging-Mouse-WMB-taxonomy",
            "Zhuang-ABCA-1",
            "Zhuang-ABCA-1-CCF",
            "Zhuang-ABCA-2",
            "Zhuang-ABCA-2-CCF",
            "Zhuang-ABCA-3",
            "Zhuang-ABCA-3-CCF",
            "Zhuang-ABCA-4",
            "Zhuang-ABCA-4-CCF",
        ]

    def test_list_metadata_files(self):
        """Test listing the files in a metadata directory."""
        with open(self.manifest_path, "r") as jfile:
            manifest = Manifest(cache_dir=self.cache_dir, json_input=jfile)

        assert manifest.list_metadata_files("Allen-CCF-2020") == [
            "parcellation",
            "parcellation_term",
            "parcellation_term_set",
            "parcellation_term_set_membership",
            "parcellation_term_with_counts",
            "parcellation_to_parcellation_term_membership",
            "parcellation_to_parcellation_term_membership_acronym",
            "parcellation_to_parcellation_term_membership_blue",
            "parcellation_to_parcellation_term_membership_color",
            "parcellation_to_parcellation_term_membership_green",
            "parcellation_to_parcellation_term_membership_name",
            "parcellation_to_parcellation_term_membership_red",
        ]

        with pytest.raises(
            DataTypeNotInDirectory,
            match=r"No metadata files found in directory WMB-10Xv2.",
        ):
            manifest.list_metadata_files("WMB-10Xv2")

    def test_list_expression_matrix_files(self):
        """List the data files in a directory."""
        with open(self.manifest_path, "r") as jfile:
            manifest = Manifest(cache_dir=self.cache_dir, json_input=jfile)

        assert manifest.list_expression_matrix_files("Zhuang-ABCA-1") == [
            "Zhuang-ABCA-1/log2",
            "Zhuang-ABCA-1/raw",
        ]

        with pytest.raises(
            DataTypeNotInDirectory,
            match=r"No expression_matrices files found in directory WMB-10X.",
        ):
            manifest.list_expression_matrix_files("WMB-10X")

    def test_list_image_volume_files(self):
        """List the image volume files in a directory."""
        with open(self.manifest_path, "r") as jfile:
            manifest = Manifest(cache_dir=self.cache_dir, json_input=jfile)
        assert manifest.list_image_volume_files("Allen-CCF-2020") == [
            "annotation_10",
            "annotation_25",
            "annotation_boundary_10",
            "annotation_boundary_25",
            "average_template_10",
            "average_template_25",
        ]

        with pytest.raises(
            DataTypeNotInDirectory,
            match=r"No image_volumes files found in directory WMB-10X.",
        ):
            manifest.list_image_volume_files("WMB-10X")

    def test_list_mapmycells_files(self):
        """List the image volume files in a directory."""
        with open(self.manifest_path, "r") as jfile:
            manifest = Manifest(cache_dir=self.cache_dir, json_input=jfile)
        assert manifest.list_mapmycells_files("WHB-10Xv3") == [
            "precomputed_stats.siletti.training",
            "query_markers.n10.20240221800",
        ]

        with pytest.raises(
            DataTypeNotInDirectory,
            match=r"No mapmycells files found in directory WMB-10X.",
        ):
            manifest.list_mapmycells_files("WMB-10Xv2")

    def test_metadata_file_attributes(self):
        """Test that Manifestget_file_attributes returns the
        correct CacheFileAttributes object for a metadata file.
        """
        cache_path = Path(self.cache_dir)
        with open(self.manifest_path, "r") as jfile:
            manifest = Manifest(cache_dir=cache_path, json_input=jfile)

        file_obj = manifest.get_file_attributes(
            directory="Allen-CCF-2020", file_name="parcellation"
        )
        assert (
            file_obj.url
            == "https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/metadata/Allen-CCF-2020/20230630/parcellation.csv"
        )  # noqa: E501
        assert file_obj.version == "20230630"
        assert file_obj.file_size == 41197
        assert (
            file_obj.local_path
            == (
                cache_path / "metadata/Allen-CCF-2020/20230630/parcellation.csv"
            ).resolve()
        )  # noqa: E501
        assert file_obj.file_type == "csv"
        assert (
            file_obj.relative_path
            == "metadata/Allen-CCF-2020/20230630/parcellation.csv"
        )  # noqa: E501
        assert file_obj.file_hash == "aea6f6925d7c84f4e5a2d022cbc9c7bb"

    def test_image_volume_file_attributes(self):
        """Test that Manifest.get_file_attributes returns the
        correct CacheFileAttributes object for an image_volume file.
        """
        cache_path = Path(self.cache_dir)
        with open(self.manifest_path, "r") as jfile:
            manifest = Manifest(cache_dir=cache_path, json_input=jfile)

        file_obj = manifest.get_file_attributes(
            directory="MERFISH-C57BL6J-638850-CCF",
            file_name="resampled_annotation_boundary",
        )
        assert (
            file_obj.url
            == "https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/image_volumes/MERFISH-C57BL6J-638850-CCF/20230630/resampled_annotation_boundary.nii.gz"
        )  # noqa: E501
        assert file_obj.version == "20230630"
        assert file_obj.file_size == 1548196
        assert (
            file_obj.local_path
            == (
                cache_path
                / "image_volumes/MERFISH-C57BL6J-638850-CCF/20230630/resampled_annotation_boundary.nii.gz"
            ).resolve()
        )  # noqa: E501
        assert file_obj.file_type == "nii.gz"
        assert (
            file_obj.relative_path
            == "image_volumes/MERFISH-C57BL6J-638850-CCF/20230630/resampled_annotation_boundary.nii.gz"
        )  # noqa: E501
        assert file_obj.file_hash == "1ce4be21528fa6cbfb462a117552477d"

    def test_expression_matrix_file_attributes(self):
        """Test that Manifest.get_file_attributes returns the
        correct CacheFileAttributes object for a expression_matrix file.
        """
        cache_path = Path(self.cache_dir)
        with open(self.manifest_path, "r") as jfile:
            manifest = Manifest(cache_dir=cache_path, json_input=jfile)

        file_obj = manifest.get_file_attributes(
            directory="WMB-10Xv2", file_name="WMB-10Xv2-Isocortex-2/log2"
        )
        assert (
            file_obj.url
            == "https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/expression_matrices/WMB-10Xv2/20230630/WMB-10Xv2-Isocortex-2-log2.h5ad"
        )  # noqa: E501
        assert file_obj.version == "20230630"
        assert file_obj.file_size == 9444387082
        assert (
            file_obj.local_path
            == (
                cache_path
                / "expression_matrices/WMB-10Xv2/20230630/WMB-10Xv2-Isocortex-2-log2.h5ad"
            ).resolve()
        )  # noqa: E501
        assert file_obj.file_type == "h5ad"
        assert (
            file_obj.relative_path
            == "expression_matrices/WMB-10Xv2/20230630/WMB-10Xv2-Isocortex-2-log2.h5ad"
        )  # noqa: E501
        assert file_obj.file_hash == "6cf8b3556e625b090c196ff5bb5f6cdd"

        with pytest.raises(
            KeyError, match=r"File WMB-10Xv2-Isocortex-2 found in directory but"
        ):
            manifest.get_file_attributes(
                directory="WMB-10Xv2", file_name="WMB-10Xv2-Isocortex-2"
            )

    def test_expression_matrix_file_attributes(self):
        """Test that Manifest.get_file_attributes returns the
        correct CacheFileAttributes object for a expression_matrix file.
        """
        cache_path = Path(self.cache_dir)
        with open(self.manifest_path, "r") as jfile:
            manifest = Manifest(cache_dir=cache_path, json_input=jfile)

        file_obj = manifest.get_file_attributes(
            directory="WMB-10Xv2", file_name="WMB-10Xv2-Isocortex-2/log2"
        )
        assert (
            file_obj.url
            == "https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/expression_matrices/WMB-10Xv2/20230630/WMB-10Xv2-Isocortex-2-log2.h5ad"
        )  # noqa: E501
        assert file_obj.version == "20230630"
        assert file_obj.file_size == 9444387082
        assert (
            file_obj.local_path
            == (
                cache_path
                / "expression_matrices/WMB-10Xv2/20230630/WMB-10Xv2-Isocortex-2-log2.h5ad"
            ).resolve()
        )  # noqa: E501
        assert file_obj.file_type == "h5ad"
        assert (
            file_obj.relative_path
            == "expression_matrices/WMB-10Xv2/20230630/WMB-10Xv2-Isocortex-2-log2.h5ad"
        )  # noqa: E501
        assert file_obj.file_hash == "6cf8b3556e625b090c196ff5bb5f6cdd"

        with pytest.raises(
            KeyError, match=r"File WMB-10Xv2-Isocortex-2 found in directory but"
        ):
            manifest.get_file_attributes(
                directory="WMB-10Xv2", file_name="WMB-10Xv2-Isocortex-2"
            )

    def test_mapmycells_file_attributes(self):
        """Test that Manifest.get_file_attributes returns the
        correct CacheFileAttributes object for a expression_matrix file.
        """
        cache_path = Path(self.cache_dir)
        with open(self.manifest_path, "r") as jfile:
            manifest = Manifest(cache_dir=cache_path, json_input=jfile)

        file_obj = manifest.get_file_attributes(
            directory="WHB-10Xv3", file_name="precomputed_stats.siletti.training"
        )
        assert (
            file_obj.url
            == "https://allen-brain-cell-atlas.s3.us-west-2.amazonaws.com/mapmycells/WHB-10Xv3/20240831/precomputed_stats.siletti.training.h5"
        )  # noqa: E501
        assert file_obj.version == "20240831"
        assert file_obj.file_size == 8724563136
        assert (
            file_obj.local_path
            == (
                cache_path
                / "mapmycells/WHB-10Xv3/20240831/precomputed_stats.siletti.training.h5"
            ).resolve()
        )  # noqa: E501
        assert file_obj.file_type == "h5"
        assert (
            file_obj.relative_path
            == "mapmycells/WHB-10Xv3/20240831/precomputed_stats.siletti.training.h5"
        )  # noqa: E501
        assert file_obj.file_hash == "dcea6d89cfb4c5db21e8d5b9a876d22b"

    def test_get_file_attributes_rasies(self):
        """Test that Manifest.get_file_attributes raise when a file is not
        found in the directory.
        """
        cache_path = Path(self.cache_dir)
        with open(self.manifest_path, "r") as jfile:
            manifest = Manifest(cache_dir=cache_path, json_input=jfile)

        with pytest.raises(
            KeyError,
            match=r"File WMB-10Xv2-Isocortex-2 not found in directory WMB-10X.",  # noqa: E501
        ):
            manifest.get_file_attributes(
                directory="WMB-10X", file_name="WMB-10Xv2-Isocortex-2"
            )

    def test_get_directory_size(self):
        """
        Test that the correct directory size is returned for a given directory
        in the manifest.
        """
        metadata_dir = "WMB-10X"
        data_dir = "WMB-10Xv3"
        small_dir = "Allen-CCF-2020"
        cache_path = Path(self.cache_dir)
        with open(self.manifest_path, "r") as jfile:
            manifest = Manifest(cache_dir=cache_path, json_input=jfile)

        ans = manifest.get_directory_metadata_size(metadata_dir)
        assert ans == "2.53 GB"

        ans = manifest.get_directory_expression_matrix_size(data_dir)
        assert ans == "176.41 GB"

        ans = manifest.get_directory_image_volume_size(small_dir)
        assert ans == "417.02 MB"

        ans = manifest.get_directory_mapmycells_size(metadata_dir)
        assert ans == "1.29 GB"
