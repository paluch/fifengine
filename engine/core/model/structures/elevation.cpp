/***************************************************************************
 *   Copyright (C) 2005-2007 by the FIFE Team                              *
 *   fife-public@lists.sourceforge.net                                     *
 *   This file is part of FIFE.                                            *
 *                                                                         *
 *   FIFE is free software; you can redistribute it and/or modify          *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 *   This program is distributed in the hope that it will be useful,       *
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
 *   GNU General Public License for more details.                          *
 *                                                                         *
 *   You should have received a copy of the GNU General Public License     *
 *   along with this program; if not, write to the                         *
 *   Free Software Foundation, Inc.,                                       *
 *   51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA              *
 ***************************************************************************/

// Standard C++ library includes
#include <string>

// 3rd party library includes
#include <boost/lexical_cast.hpp>

// FIFE includes
// These includes are split up in two parts, separated by one empty line
// First block: files included from the FIFE root src directory
// Second block: files included from the same folder
#include "util/debugutils.h"
#include "util/purge.h"
#include "util/exception.h"

#include "elevation.h"
#include "map.h"
#include "layer.h"

namespace FIFE { namespace model {

	Elevation::Elevation(Map* map) 
		: AttributedClass("map_elevation"),
		m_map(map),
		m_reference_layer(0) {
	}

	Elevation::~Elevation() {

	}

	Map* Elevation::getMap() {
		return m_map;	
	}

	size_t Elevation::getNumLayers() const {
		return m_layers.size();
	}

	Layer* Elevation::addLayer(Geometry* geometry) {
		Layer* layer = new Layer(this, geometry);
		m_layers.push_back(layer);
		return layer;
	}

	void Elevation::removeLayer(Layer* layer) {
		std::vector<Layer*>::iterator it = m_layers.begin();
		for(; it != m_layers.end(); ++it) {
			if((*it) == layer) {
				delete *it;
				m_layers.erase(it);
				return ;
			}
		}
	}

	void Elevation::clearLayers() {
		purge(m_layers);
		m_layers.clear();
	}

	void Elevation::update() {
		std::vector<Layer*>::iterator it = m_layers.begin();
		for(; it != m_layers.end(); ++it) {
			(*it)->update();
		}
	}


} } //FIFE::model
