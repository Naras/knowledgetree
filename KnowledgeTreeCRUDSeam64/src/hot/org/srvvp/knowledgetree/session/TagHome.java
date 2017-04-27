package org.srvvp.knowledgetree.session;

import org.srvvp.knowledgetree.entity.*;
import java.util.ArrayList;
import java.util.List;
import org.jboss.seam.annotations.In;
import org.jboss.seam.annotations.Name;
import org.jboss.seam.framework.EntityHome;

@Name("tagHome")
public class TagHome extends EntityHome<Tag> {

	@In(create = true)
	TagHome tagHome;

	public void setTagId(String id) {
		setId(id);
	}

	public String getTagId() {
		return (String) getId();
	}

	@Override
	protected Tag createInstance() {
		Tag tag = new Tag();
		return tag;
	}

	public void load() {
		if (isIdDefined()) {
			wire();
		}
	}

	public void wire() {
		getInstance();
	}

	public boolean isWired() {
		return true;
	}

	public Tag getDefinedInstance() {
		return isIdDefined() ? getInstance() : null;
	}

	public List<Tag> getTags() {
		return getInstance() == null ? null : new ArrayList<Tag>(getInstance()
				.getTags());
	}

}
