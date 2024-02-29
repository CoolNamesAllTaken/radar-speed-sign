jQuery(function () {
  /* Change the CTA for pages with PG in it.*/
  if (jQuery(".bwg-container").length) {
    var html = '<div class="twb_admin_bar_menu_header">';
    html += '<img class="twb_menu_logo" src="' + twb.plugin_url + '/assets/images/logo_white.svg" />';
    html += '<div class="twb_menu_logo">Optimize Images</div>';
    html += '</div>';
    jQuery(".twb_admin_bar_menu").html(html).on("click", function () {
      window.open(twb.href, '_blank');
    });
    jQuery(".twb_admin_bar_menu_main").remove();
  }

  /* Is score check in progress.*/
  twb_inprogress = false;

  /* Check if any score check is in progress.*/
  jQuery(".twb-notoptimized").each(function () {
    if (jQuery(this).data("status") == 'inprogress') {
      /* Disable score check button.*/
      twb_disable_check();
    }
  });

  /* Add check score action to the button in page/posts list,
    if there is no inprogress action.*/
  jQuery(".twb-notoptimized .twb_check_score_button").on("click", function () {
    if (!twb_inprogress) {
      twb_check_score(this);
    }
  });

  /* Add a hover action to show dismiss tooltip.*/
  jQuery("th[id^='twb-speed-']").hover(function () {
      jQuery(this).find(".twb-dismiss-container").removeClass("twb-hidden");
    },
    function () {
      jQuery(this).find(".twb-dismiss-container").addClass("twb-hidden");
    });

  /* Add a hover action to show page score.*/
  jQuery(".twb-see-score").hover(function () {
      jQuery(this).parent().parent().find(".twb-score-container").removeClass("twb-hidden");
    },
    function () {
      jQuery(this).parent().parent().find(".twb-score-container").addClass("twb-hidden");
    });
  jQuery(".twb-score-container:not(.twb_admin_bar_menu_content .twb-score-container), .twb-score-disabled-container").hover(function () {
      jQuery(this).removeClass("twb-hidden");
    },
    function () {
      jQuery(this).addClass("twb-hidden");
    });

  /* Draw circle on given scores.*/
  jQuery(".twb-score-circle").each(function () {
    twb_draw_score_circle(this);
  });

  /* Show/hide Image optimizer menu content container */
  jQuery("#wp-admin-bar-twb_adminbar_info").mouseenter(function(){
    jQuery(".twb_admin_bar_menu_main .twb-score-container").removeClass("twb-hidden");
    jQuery(".twb_admin_bar_menu_main").removeClass("twb-hidden");
  }).mouseleave(function() {
    jQuery(".twb_admin_bar_menu_main").addClass("twb-hidden");
  });


  /* Draw circle on given scores.*/
  jQuery('.twb-score-circle').each(function () {
    twb_draw_score_circle(this);
  });

  if( jQuery(".twb_admin_bar_menu.twb_backend span").hasClass("twb_backend_optimizing_logo") ) {
    /* Run ajax every 30 seconds to check if score counted */
    twb_run_notif_check = setInterval( twb_run_notif_check, 30000 );
  }
});

/* Run ajax to check score counting status and show notification */
function twb_run_notif_check() {
  jQuery.ajax({
    type: "POST",
    url: twb.ajax_url,
    data: {
      action: "twb_notif_check",
      twb_nonce: twb.nonce,
    }
  }).success(function (results) {
    var result = jQuery.parseJSON(results);
    if (result.html != "") {
      /* Show notification popup and change menu icon and text from loading to Not optimised */
      if ( result.changeLogo == 1 ) {
        jQuery(".twb_admin_bar_menu_header span").addClass("twb_counted");
      }
      jQuery("#wp-admin-bar-twb_adminbar_info").append(result.html);
      jQuery(".twb_admin_bar_menu_content .twb-score-container").removeClass("twb-hidden");
      jQuery(".twb_admin_bar_menu_content .twb-score-container .twb-score-circle").each(function () {
        twb_draw_score_circle(this);
      });
      clearInterval(twb_run_notif_check);
    }
  }).error(function () {
      clearInterval(twb_run_notif_check);
  });

}

function twb_disable_check() {
  twb_inprogress = true;
  /* Add a hover action to show disabled notification.*/
  jQuery(".twb-notoptimized").hover(function () {
      jQuery(this).parent().find(".twb-score-disabled-container").removeClass("twb-hidden");
    },
    function () {
      jQuery(this).parent().find(".twb-score-disabled-container").addClass("twb-hidden");
    });
}
/**
 * Optimize the page.
 * @param that
 */
function twb_check_score(that) {
  var post_id = jQuery(that).data("post_id");
  var parent = jQuery(that).parent().parent().parent();
  //var parent = jQuery(that).closest(".twb-score-container").parent();
  /* Class add loading near admin bar menu */
  jQuery(".twb_admin_bar_menu.twb_frontend").addClass("twb_score_inprogress");

  /* If the action is not called with reload button.*/
  if (parent.find(".twb-optimized").hasClass("twb-hidden")) {
    /* Do not show loading in list.*/
    parent.find(".twb-optimizing").removeClass("twb-hidden");
  }
  else {
    /* Show loading on reload buttons.*/
    parent.find(".twb-score-overlay").removeClass("twb-hidden");
    parent.find(".twb-score-overlay div").removeClass("twb-reload").addClass("twb-loader");
  }

  parent.find(".twb-notoptimized").addClass("twb-hidden");

  /* In case of Elementor */
  if( parent.hasClass("twb_elementor_settings_content") ) {
    jQuery(".twb_elementor_control_title").text(twb.checking).removeClass("twb_not_optimized").prepend("<span class='twb_inprogress'></span>");
  }

  /* Disable score check button.*/
  twb_disable_check();

  jQuery.ajax({
    url: twb.ajax_url,
    type: "POST",
    dataType: 'json',
    data: {
      action: "twb_check_score",
      post_id: post_id,
      twb_nonce: twb.nonce
    },
    success: function (data) {
      if (data.error) {
        /* Show reload buttons on failure.*/
        parent.find(".twb-score-overlay").removeClass("twb-hidden");
        parent.find(".twb-score-overlay div").removeClass("twb-loader").addClass("twb-reload");
      }
      else {
        parent.find(".twb-score-overlay").addClass("twb-hidden");
        var desktop = parent.find(".twb-score-desktop").find(".twb-score-circle");
        desktop.data(
          {
            "score": data.desktop_score,
            "tti": data.desktop_tti,
          });
        twb_draw_score_circle(desktop);
        var mobile = parent.find(".twb-score-mobile").find(".twb-score-circle");
        mobile.data(
          {
            "score": data.mobile_score,
            "tti": data.mobile_tti,
          });
        twb_draw_score_circle(mobile);
      }
    },
    error: function (xhr, textStatus, errorThrown) {
      /* Show reload buttons on failure.*/
      parent.find(".twb-score-overlay").removeClass("twb-hidden");
      parent.find(".twb-score-overlay div").removeClass("twb-loader").addClass("twb-reload");
    },
    complete: function (xhr, textStatus) {
      /* Hide optimizing container, show See score container.*/
      parent.find(".twb-optimizing").addClass("twb-hidden");
      parent.find(".twb-optimized").removeClass("twb-hidden");

      jQuery("#wpadminbar .twb-optimized .twb-score-container").removeClass("twb-hidden");
      jQuery("#wpadminbar .twb_admin_bar_menu").removeClass("twb_score_inprogress");
      jQuery("#wpadminbar .twb_menu_logo").remove();
      jQuery("#wpadminbar .twb_not_optimized_logo").removeClass("twb-hidden");
      jQuery("#wpadminbar .twb_admin_bar_menu_header").addClass("twb_not_optimized");

      /* Remove disabled action.*/
      twb_inprogress = false;
      jQuery(".twb-notoptimized").hover(function () {
        jQuery(this).parent().find(".twb-score-disabled-container").addClass("twb-hidden");
      });

      /* In case of Elementor */
      if( parent.hasClass("twb_elementor_settings_content") ) {
        jQuery(".twb_elementor_control_title").text(twb.notoptimized).remove("span.twb_inprogress").addClass("twb_not_optimized");
      }
    }
  });
}

/**
 * Draw circle on given score.
 * @param that
 */
function twb_draw_score_circle(that) {
  var score = parseInt(jQuery(that).data('score'));
  var size = parseInt(jQuery(that).data('size'));
  var thickness = parseInt(jQuery(that).data('thickness'));
  var color = score <= 49 ? "rgb(253, 60, 49)" : (score >= 90 ? "rgb(12, 206, 107)" : "rgb(255, 164, 0)");
  jQuery(that).parent().find('.twb-load-time').html(jQuery(that).data('tti'));
  var _this = that;
  jQuery(_this).circleProgress({
    value: score / 100,
    size: size,
    startAngle: -Math.PI / 4 * 2,
    lineCap: 'round',
    emptyFill: "rgba(255, 255, 255, 0)",
    thickness: thickness,
    fill: {
      color: color
    }
  }).on('circle-animation-progress', function (event, progress) {
    var content = '<span class="twb-score0"></span>';
    if (score != 0) {
      content = Math.round(score * progress);
    }
    jQuery(that).find('.twb-score-circle-animated').html(content).css({"color": color});
    jQuery(that).find('canvas').html(Math.round(score * progress));
  });
}

/* Adding button in Elementor edit panel navigation view */
function twb_add_elementor_button() {
  window.elementor.modules.layouts.panel.pages.menu.Menu.addItem({
    name: twb.title,
    icon: "twb-element-menu-icon",
    title: twb.title,
    type: "page",
    callback: () => {
      try {
        window.$e.route("panel/page-settings/twb_optimize")
      } catch (e) {
        window.$e.route("panel/page-settings/settings"), window.$e.route("panel/page-settings/twb_optimize")
      }
    }
  }, "more")
}

jQuery(window).on("elementor:init", () => {
  window.elementor.on("panel:init", () => {
    setTimeout(twb_add_elementor_button)
  })
});
