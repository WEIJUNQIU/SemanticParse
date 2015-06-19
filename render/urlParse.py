# -*-coding:utf-8-*-
import sys, os
reload(sys)
sys.setdefaultencoding( "utf-8" )
import re
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *


# 面包屑：1，标题：2，详情：3
# edomain: 域名
# eclass: 类名
# eid: id名
# nextclass: 下一类名
# nextid: 下一id名
# other: 附加信息
class urlParse():
    def get_label(self, edomain, eclass, eid, nextclass, nextid, tagname, other):
        if edomain == '0478g':
            if eid == 'deal-intro' and nextid == 'deal-stuff':
                return 2
            elif eclass == 'main' and eid == 'team_main_side' and nextid == 'team_partner_side_0':
                return 3
            else:
                return 0
        elif edomain == '0790tg':
            if eclass == 'sp-content fix':
                return 2
            elif eclass == 'deal-detail mod':
                return 3
            else:
                return 0
        elif edomain == '0912158':
            if eid == 'deal-intro' and eclass == 'cf':
                return 2
            elif eclass == 'blk detail' and nextid == 'team_partner_side_0':
                return 3
            else:
                return 0
        elif edomain == 'sansantuan':
            if eid == 'deal-intro' and eclass == 'cf':
                return 2
            elif eclass == 'main' and other == 'padding:15px; width:670px; background-color:#FFFFFF;':
                return 3
            else:
                return 0
        elif edomain == 'haochimei':
            if other == 'padding:0px 0px 9px 10px; font-size:12px; color:#000;':
                return 1
            elif eclass == 'g_outline':
                return 2
            elif eclass == 'content':
                return 3
            else:
                return 0
        elif edomain == 'tuanyanan':
            if eid == 'deal-intro' and eclass == 'cf':
                return 2
            elif eid == 'n_d_field' and eclass == 'n_d_field':
                return 3
            else:
                return 0
        elif edomain == 'higo':
            if eid == 'deal-intro' and eclass == 'cf':
                return 2
            elif eclass == 'lazy box_main':
                return 3
            else:
                return 0
        elif edomain == 'taobao':
            if eclass == 'header clearfix':
                return 1
            elif eclass == 'clearfix' and tagname!= 'DD':
                return 2
            elif eclass == 'detail-con J_detailCon dd-content':
                return 3
            else:
                return 0
        elif edomain == 'jd':
            if eclass == 'breadcrumb':
                return 1
            elif eid == 'product-intro' or eclass == 'm-item-grid clearfix':
                return 2
            elif eid == 'product-detail-1' or eid == 'product-detail':
                return 3
            else:
                return 0
        elif edomain == 'dianping':
            if eclass == 'summary summary-comments-big J_summary Fix':
                return 2
            elif eclass == 'box-cont tradingQA Fix':
                return 3
            else:
                return 0
        elif edomain == 'meituan':
            if eclass == 'bread-nav':
                return 1
            elif eclass == 'deal-component-container' \
                    or eclass=='deal-component-container deal-component-container--appoint'\
                    or eclass == 'poi-header cf':
                return 2
            elif eclass == 'blk detail' or eclass == 'poi-infobox col-d-15 col-l-18 col-m-15 col-last':
                return 3
            else:
                return 0
        elif edomain == 'qunar':
            if eclass == 'Qt_bread Qt_Tahoma' or eclass == 'pt-location':
                return 1
            elif eclass == 'Qt_detail js-detail clearfix' or eclass == 'pt-major clrfix':
                return 2
            elif eclass == 'Qt_fl Qt_left' or eclass == 'pt-cont-notice pt-detail-wrap':
                return 3
            else:
                return 0
        elif edomain == 'tuniu':
            if eclass == 'search_nav':
                return 1
            elif eclass == 'mainPic clearfix' or eclass == 'ticket_proinf':
                return 2
            elif eclass == 'detail_con_item room_reservation':
                return 3
            else:
                return 0
        elif edomain == 'tmall':
            if eclass == 'tm-clear' and nextid == 'J_SpuMore_Act':
                return 2
            elif eid == 'description' and eclass == 'J_DetailSection tshop-psm tshop-psm-bdetaildes':
                return 3
            else:
                return 0
        elif edomain == 'nuomi':
            if eclass == 'crumb-list clearfix':
                return 1
            elif eclass == 'w-item-info clearfix':
                return 2
            elif eclass == 'item-info-detail j-item-content' and nextid == 'j-info-consum-tip':
                return 3
            else:
                return 0
        elif edomain == 'ctrip':
            if eclass == 'crumbs':
                return 1
            elif eclass == 'detail-modebox detail-info-box':
                return 2
            elif eclass == 'detail-modebox product-detail':
                return 3
            else:
                return 0
        elif edomain == 'lashou':
            if eclass == 'breadcrumbs':
                return 1
            elif eclass == 'detail-intro cl':
                return 2
            elif eclass == 'detail-info':
                return 3
            else:
                return 0
        elif edomain == '55tuan':
            if eclass == 'Crumbs':
                return 1
            elif eclass == 'details-ui clearfix':
                return 2
            elif eclass == 'details-msgtxt'and eid == 'goodsAll_info_div':
                return 3
            else:
                return 0

        elif edomain == 'amazon':
            if eclass == "a-horizontal a-size-small":
                return 1
            elif eclass == 'centerColAlign' and eid == 'centerCol':
                return 2
            elif eid == 'detail_bullets_id':
                return 3
            else:
                return 0
        elif edomain == 'dangdang':
            if eclass == 'breadcrumb':
                return 1
            elif eclass == 'pic_info clearfix':
                return 2
            elif eclass == 'pro_content':
                return 3
            else:
                return 0
        elif edomain == 'suning':
            if eclass == 'breadcrumb':
                return 1
            elif eclass == 'proinfo-container clearfix':
                return 2
            elif eclass == 'tabarea-content' and eid == 'J-procon-desc':
                return 3
            else:
                return 0
        elif edomain == 'gome':
            if eclass == 'local':
                return 1
            elif eclass == 'wbox oh':
                return 2
            elif eclass == 'prdDescOut':
                return 3
            else:
                return 0
        elif edomain == 'vmall':
            if eclass == 'breadcrumb-area fcn':
                return 1
            elif eclass == 'pro-summary-area clearfix':
                return 2
            elif eclass == 'pro-detail-tab-area pro-feature-area':
                return 3
            else:
                return 0
        elif edomain == 'vancl':
            if eclass == 'breadNav':
                return 1
            elif eclass == 'danpinArea':
                return 2
            elif eclass == 'sideBarSettabArea':
                return 3
            else:
                return 0
        elif edomain == 'jumei':
            if eclass == 'location':
                return 1
            elif eid == 'detail_top':
                return 2
            elif eid == 'detail_info_box':
                return 3
            else:
                return 0
        elif edomain == 'eelly':
            if eclass == 'curlocal text-ellipsis':
                return 1
            elif eclass == 'pd_rightbar':
                return 2
            elif eclass == 'goods_des_box':
                return 3
            else:
                return 0
        elif edomain == 'wbiao':
            if eid == 'bread_crumb':
                return 1
            elif eclass == 'v-1225-1000' and eid == 'goods':
                return 2
            elif eclass == 'column' and eid == 'desc':
                return 3
            else:
                return 0
        elif edomain == 'womai':
            if eclass == 'detail-breadcrumbnav width':
                return 1
            elif eclass == 'detail-top':
                return 2
            elif eclass == 'prod-detail':
                return 3
            else:
                return 0
        elif edomain == 'moonbasa':
            if eclass == 'this_page':
                return 1
            elif eclass == 'p_info':
                return 2
            elif eclass == 'right':
                return 3
            else:
                return 0
        elif edomain == 'yougou':
            if eclass == 'curLct ngoods_bor':
                return 1
            elif eclass == 'goodsCon fr':
                return 2
            elif eclass == 'bd' and nextclass == 'price_explain mt5':
                return 3
            else:
                return 0
        elif edomain == 'zol':
            if eclass == 'zs-deal-detail':
                return 2
            elif eclass == 'zs-goods-detail':
                return 3
            else:
                return 0
        elif edomain == 'yintai':
            if eclass == 'crumbs':
                return 1
            elif eclass == 'y-pro-place':
                return 2
            elif eclass == 'yp-detail-con':
                return 3
            else:
                return 0
        elif edomain == 'xiu':
            if eclass == 'dh':
                return 1
            elif eclass == 'con_main':
                return 2
            elif eclass == 'contents' and nextclass == 'container':
                return 3
            else:
                return 0
        elif edomain == 'okbuy':
            if eclass == 'prodConTopInTit':
                return 1
            elif eclass == 'prodConTopIn':
                return 2
            elif eid == 'prInLeftImgAndAttr':
                return 3
            else:
                return 0
        elif edomain == 'paixie':
            if eclass == 'location':
                return 1
            elif eclass == 'proinfo':
                return 2
            elif eclass == 'detailsimg':
                return 3
            else:
                return 0
        elif edomain == 'spider':
            if eclass == 'm1_qgsp_bt':
                return 1
            elif eclass == 'm1_qgsp':
                return 2
            elif eclass == 'cpxx_spxx':
                return 3
            else:
                return 0
        elif edomain == 'jiuxian':
            if eclass == 'detail-guide':
                return 1
            elif eclass == 'detail-box1':
                return 2
            elif eclass == 'detail_switch clearfix':
                return 3
            else:
                return 0
        elif edomain == 'shangpin':
            if eclass == 'sp_crumb':
                return 1
            elif eclass == 'spDetail_main':
                return 2
            elif eclass == 'spTabsCell clr':
                return 3
            else:
                return 0
        elif edomain == 'ehaier':
            if eclass == 'crumb' and eid == 'crumb':
                return 1
            elif eclass == 'product-info-box clearfix':
                return 2
            elif eclass == 'details-cont details-proinfo details-cont-now':
                return 3
            else:
                return 0
        elif edomain == 'sephora':
            if eid == 'widget_breadcrumb':
                return 1
            elif eclass == 'proDetBox clearFix':
                return 2
            elif eclass == 'productDetInfo mb64':
                return 3
            else:
                return 0
        elif edomain == 'homekoo':
            if eclass == 'business':
                return 1
            elif eclass == 'top_box_right':
                return 2
            elif eid == 'main_widget_1':
                return 3
            else:
                return 0
        elif edomain == 'taoxie':
            if eclass == 'crumb clr':
                return 1
            elif eclass == 'detail clr':
                return 2
            elif eclass == 't_TabDetailContent':
                return 3
            else:
                return 0
        elif edomain == '17ugo':
            if eclass == 'sjnav clearfix':
                return 1
            elif eclass == 'pro-choice border clearfix':
                return 2
            elif eclass == 'Detailscon':
                return 3
            else:
                return 0

        elif edomain == 'tiantian':
            if eclass == 'detail_mbx':
                return 1
            elif eclass == 'detail_pro clearfix':
                return 2
            elif eclass == 'detail_tab_con11 box-shadow':
                return 3
            else:
                return 0
        elif edomain == 'm6go':
            if eclass == 'breadcrumb shareW':
                return 1
            elif eclass == 'shareW productInfo':
                return 2
            elif other == 'margin-top: 10px;':
                return 3
            else:
                return 0
        elif edomain == 'yhd':
            if eclass == 'crumb clearfix' or eclass == 'mod_group_crumb clearfix':
                return 1
            elif eclass == 'fm_detail_one clearfix' or eclass == 'mod_sku clearfix':
                return 2
            elif eclass == 'desitem' or eid == 'productDescTabListDiv':
                return 3
            else:
                return 0

        elif edomain == 'vip':
            if eclass == 'M-class':
                return 1
            elif eclass == 'FW-product clearfix':
                return 2
            elif eclass == 'M-detailCon':
                return 3
            else:
                return 0
        elif edomain == 'yaofang':
            if tagname=='div' and eclass == 'title':
                return 1
            elif eclass == 'topCon':
                return 2
            elif eclass == 'divBox message':
                return 3
            else:
                return 0
        elif edomain == '5lux':
            if eid == 'gdetail_con':
                return 2
            elif eclass == 'goods_detail tab_list':
                return 3
            else:
                return 0
        elif edomain == 'letao':
            if eid == 'ltlinknav':
                return 1
            elif eid == 'buyinfo':
                return 2
            elif eid == 'shoeimages':
                return 3
            else:
                return 0
        elif edomain == 'zhen':
            if eclass == 'location_show clr':
                return 1
            elif eclass == 'detail_main clearfix':
                return 2
            elif eclass == 'spxq':
                return 3
            else:
                return 0

        elif edomain == 'uniqlo':
            if eclass == 'detail-bd clearfix':
                return 2
            elif eid == 'description':
                return 3
            else:
                return 0
        elif edomain == 'masamaso':
            if eclass == 'info_nav':
                return 1
            elif eclass == 'goods_info_box clearfix':
                return 2
            elif eclass == 'sp_l_shadow':
                return 3
            else:
                return 0
        elif edomain == 'yixun':
            if eclass == 'mod_crumb':
                return 1
            elif eclass == 'grid_c1 xcontent_row2':
                return 2
            elif eid == 'x_mod_tab_con intro-main':
                return 3
            else:
                return 0
        elif edomain == 'feiniu':
            if eclass == 'topic-path':
                return 1
            elif eclass == 'product-detail-content':
                return 2
            elif eclass == 'desc-block desc-b1':
                return 3
            else:
                return 0

        elif edomain == 'gojiaju':
            if eclass == 'line_positionleft':
                return 1
            elif eclass == 'jj_dir_top':
                return 2
            elif eclass == 'tabcon':
                return 3
            else:
                return 0
        elif edomain == 'hitao':
            if eclass == 'bread-crumbs':
                return 1
            elif eclass == 'product-container clearfix':
                return 2
            elif eid == 'detail-content':
                return 3
            else:
                return 0
        elif edomain == 'manzuo':
            if eclass == 'small_nav':
                return 1
            elif eclass == 'index_hd_top blank border1':
                return 2
            elif eclass == 'con_lbmleft':
                return 3
            else:
                return 0
        elif edomain == 'elong':
            if eclass == 'grid grid2 dts_f':
                return 1
            elif eclass == 'hotel_wrap':
                return 2
            elif eclass == 'g_tab_con order_con':
                return 3
            else:
                return 0
        else:
            return 0
        # elif edomain == 'livingsocial':
        #     pass
        # elif edomain == 'groupon':
        #     pass
        pass

    def parse_domain(self, url):
        print url
        do = re.search(r"(?<=.).+?(?=.com)", str(url), re.M)
        if do is None:
            do = re.search(r"(?<=.).+?(?=.cn)", str(url), re.M)
        if do is None:
            do = re.search(r"(?<=.).+?(?=.net)", str(url), re.M)
        return do.group(0).split('.')[-1]

