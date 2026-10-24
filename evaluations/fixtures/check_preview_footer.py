import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch
from PIL import ImageDraw


ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('preview',ROOT/'master-skills/github-social-preview/scripts/generate_preview.py')
preview=importlib.util.module_from_spec(spec)
spec.loader.exec_module(preview)


class PreviewFooterTests(unittest.TestCase):
    def render_and_check(self,language,width,theme='builder-green'):
        config=preview.load_config()
        colors=preview.pick_theme(config,theme,None)['colors']
        pills=[];language_text=[];dots=[]
        rounded=preview.draw_rounded_rect
        text=ImageDraw.ImageDraw.text
        ellipse=ImageDraw.ImageDraw.ellipse
        def capture_pill(draw,xy,*args,**kwargs):
            if kwargs.get('fill')==preview.hex_to_rgb(colors['tag_bg']):pills.append(xy)
            return rounded(draw,xy,*args,**kwargs)
        def capture_text(draw,xy,value,*args,**kwargs):
            if language and kwargs.get('fill')==preview.hex_to_rgb(colors['text_secondary']) and xy[1]>width*.3:
                language_text.append(draw.textbbox(xy,value,font=kwargs['font']))
            return text(draw,xy,value,*args,**kwargs)
        def capture_dot(draw,xy,*args,**kwargs):
            if language and kwargs.get('fill')==preview.hex_to_rgb(preview.LANGUAGE_COLORS.get(language,'#8b949e')):dots.append(xy)
            return ellipse(draw,xy,*args,**kwargs)
        with patch.object(preview,'draw_rounded_rect',capture_pill),patch.object(ImageDraw.ImageDraw,'text',capture_text),patch.object(ImageDraw.ImageDraw,'ellipse',capture_dot):
            image=preview.generate_image('Telemetry Audit Lab Δ | Reliable Offline Endpoint Inventory Validation and Reconciliation','Validate fabricated endpoint inventories offline.', ['automation','offline-validation','inventory','PowerShell','Python'],language,config,theme=theme,width=width,height=width//2)
        self.assertTrue(pills)
        self.assertEqual(image.size,(width,width//2))
        if language:
            self.assertEqual(len(dots),1)
            self.assertEqual(len(language_text),1)
            badge=tuple((min if i<2 else max)(box[i] for box in [dots[0],language_text[0]]) for i in range(4))
            for box in pills:
                self.assertTrue(box[2]<badge[0] or box[3]<badge[1] or box[1]>badge[3])
            self.assertGreaterEqual(badge[0],width*.0625)
            self.assertLessEqual(badge[2],width-width*.0625)
            self.assertLessEqual(badge[3],width//2-width*.0625)
        return image

    def test_actual_footer_draws_do_not_intersect(self):
        for width in (640,1280):
            for language in ('Python','PowerShell','Unusually Long Language Label With Extra Words'):
                with self.subTest(width=width,language=language):self.render_and_check(language,width)

    def test_no_language_keeps_tag_space(self):
        image=self.render_and_check(None,1280,'github-dark')
        self.assertEqual(len(image.info['footer_layout']['tags']),5)

    def test_checklist_does_not_certify_uninspected_crop(self):
        image=self.render_and_check('Python',1280)
        checklist=dict(preview.build_preview_checklist(preview.load_config(),1000,image))
        self.assertTrue(checklist['crop_safety'].startswith('REVIEW'))
        self.assertEqual(checklist['tag_badge_separation'],'PASS')
        image.info['footer_layout']['tags']=[image.info['footer_layout']['language']]
        checklist=dict(preview.build_preview_checklist(preview.load_config(),1000,image))
        self.assertTrue(checklist['tag_badge_separation'].startswith('WARN'))


if __name__=='__main__':
    unittest.main(verbosity=2)
