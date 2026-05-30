from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.base_models import ConversionStatus
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling_core.types.doc.labels import DocItemLabel
import json
import os
from pathlib import Path


PAPERS_DIR = "data/papers"
JSON_DIR = "data/processed/json"
FIGURES_DIR = "data/processed/figures"


class ScientificPaperIngestor:
    def __init__(self, papers_dir: str,
                 output_dir: str,
                 figures_dir: str) -> None:
        self.papers_dir = Path(papers_dir)
        if not os.path.exists(papers_dir):
            raise FileNotFoundError(f"Directory {papers_dir} does not exist.")
        
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.figures_dir = Path(figures_dir)
        self.figures_dir.mkdir(parents=True, exist_ok=True)

        # Configure Docling to extract figures
        pipeline_options = PdfPipelineOptions()
        pipeline_options.images_scale = 2.0
        pipeline_options.generate_page_images = False
        pipeline_options.generate_picture_images = True

        self.converter = DocumentConverter(
            format_options = {
                InputFormat.PDF: PdfFormatOption(
                    pipeline_options=pipeline_options
                )
            }
            
        )

    def process_all_papers(self) -> None:
        """Finds all PDF files in the papers directory and processes them."""
        pdf_file_paths = list(self.papers_dir.glob("*.pdf"))

        if not pdf_file_paths:
            print(f"No PDF files found in {self.papers_dir}.")
            return
        
        print(f"Found {len(pdf_file_paths)} PDF files. Processing...")
        
        for pdf_path in pdf_file_paths:
            try:
                self._process_single_paper(pdf_path)
            except Exception as e:
                print(f"Error processing {pdf_path.name}: {e}")

    def _process_single_paper(self, pdf_path: Path) -> None:
        print(f"Processing {pdf_path.name}...")

        # Convert via Docling
        result = self.converter.convert(pdf_path)

        if result.status != ConversionStatus.SUCCESS:
            raise RuntimeError(f"Conversion failed for {pdf_path.name}: {result.status} : {result.error_message}")
        
        doc = result.document
        unified_nodes = []

        # Create subdirectory for current paper's figures
        paper_slug = pdf_path.stem.replace(" ", "_").lower()
        paper_figures_dir = self.figures_dir / paper_slug
        paper_figures_dir.mkdir(parents=True, exist_ok=True)

        # Track parent-child hierarchy dynamically using Python memory IDs
        # Maps Python object id(item) -> a stable string ID for your JSON
        id_map = {}

        # Iterate swquentially through the layout tree
        for item, level in doc.iterate_items():
            obj_id = id(item)
            node_id = f'node_{obj_id}'
            id_map[obj_id] = node_id

            parent_id = None
            if hasattr(item, "parent") and item.parent:
                parent_obj_id = id(item.parent)
                if parent_obj_id not in id_map:
                    parent_id = f'node_{parent_obj_id}'
                    id_map[parent_obj_id] = parent_id
                parent_id = id_map[parent_obj_id]

            node_data = {
                "id": node_id,
                "parent_id": parent_id,
                "type": "unknown",
                "text": "",
                "metadata": {
                    "page_numbers": [prov.page_no for prov in item.prov] if item.prov else []
                }
            }

            # --- CASE-WISE HANDLING BASED ON ITEM TYPE ---
            label = getattr(item, "label", None)
            item_text = getattr(item, "text", "")
            
            # Case 1: Headings
            if label == DocItemLabel.SECTION_HEADER:
                node_data["type"] = "heading"
                node_data["level"] = level
                node_data["text"] = item_text

            # Case 2: Paragraphs
            elif label == DocItemLabel.PARAGRAPH:
                node_data["type"] = "paragraph"
                node_data["text"] = item_text

            # Case 3: Equations
            elif label == DocItemLabel.FORMULA:
                node_data["type"] = "equation"
                node_data["text"] = item_text

            # Case 4: Tables
            elif label == DocItemLabel.TABLE:
                node_data["type"] = "table"
                try:
                    node_data["text"] = item.export_to_markdown()
                except Exception:
                    node_data["text"] = item_text

            # Case 5: Figures / Captions
            elif label == DocItemLabel.PICTURE:
                node_data["type"] = "figure"
                
                # Extract and save figure 
                safe_node_id = node_id
                figure_filename = f"{safe_node_id}.png"
                figure_path = paper_figures_dir / figure_filename

                try:
                    # Access the image from Docling's internal storage
                    image_element = item.get_image(doc)
                    if image_element:
                        image_element.save(figure_path)
                        node_data["metadata"]["figure_path"] = f"{paper_figures_dir} /{figure_filename}"
                except Exception as e:
                    node_data["metadata"]["figure_extraction_error"] = f"Failed to extract figure: {e}"

                node_data["text"] = "[Figure Node: Image saved to disk]"
                
            elif label in [DocItemLabel.CAPTION, DocItemLabel.TITLE]:  # Placeholder text"
                node_data["text"] = item_text
                node_data["type"] = "caption" if label == DocItemLabel.CAPTION else "title"

            # Case 6: Clean out metadata artifacts
            elif label in [DocItemLabel.PAGE_HEADER, DocItemLabel.PAGE_FOOTER]:
                continue

            else:
                node_data["type"] = "text_block"
                node_data["text"] = item_text


            # Append node if it holds content or if its valid figure metadata tracker
            if node_data["text"].strip() or "figure_path" in node_data["metadata"]:
                unified_nodes.append(node_data)

        # Build output structure
        output_payload = {
            "document_metadata": {
                "filename": pdf_path.name,
                "title": doc.name or pdf_path.stem,
                "total_elements": len(unified_nodes)
            },
            "nodes": unified_nodes
        }

        # Write JSON output
        output_json_path = self.output_dir / f"{pdf_path.stem}.json"
        with open(output_json_path, "w", encoding="utf-8") as f:
            json.dump(output_payload, f, indent=2, ensure_ascii=False)

        print(f"Finished processing {pdf_path.name}. Output saved to {output_json_path}.")
        print(f"Extracted {len(unified_nodes)} nodes, with figures saved to {paper_figures_dir}.")


def process_papers():
    ingestor = ScientificPaperIngestor(
        papers_dir=PAPERS_DIR,
        output_dir=JSON_DIR,
        figures_dir=FIGURES_DIR
    )
    ingestor.process_all_papers()


if __name__ == "__main__":
    process_papers()