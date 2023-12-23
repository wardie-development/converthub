from unittest.mock import Mock, patch

from chalicelib.basic.basic_file_entity import BasicFileEntity
from chalicelib.domain.pdf_entity import PdfEntity


class TestPdfEntity:
    @classmethod
    def setup_class(cls):
        cls.entity = PdfEntity

    def test_parent(self):
        assert issubclass(self.entity, BasicFileEntity)

    @patch("chalicelib.domain.pdf_entity.BasicFileEntity.__init__")
    def test_init(self, mock_super_init):
        mock_file_content = Mock()
        mock_file_name = Mock()
        mock_entity_id = Mock()

        self.entity(
            file_content=mock_file_content,
            file_name=mock_file_name,
            entity_id=mock_entity_id,
        )

        mock_super_init.assert_called_once_with(
            file_content=mock_file_content,
            file_name=mock_file_name,
            file_type="pdf",
            entity_id=mock_entity_id,
        )
